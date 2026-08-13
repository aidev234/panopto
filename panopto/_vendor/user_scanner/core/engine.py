import asyncio
import inspect
import concurrent.futures

from typing import List
from types import ModuleType
from user_scanner.core.result import Result
from user_scanner.core.helpers import find_category, get_scan_func, get_site_name, is_loud, load_modules, load_categories

_shared_executor = concurrent.futures.ThreadPoolExecutor(max_workers=60)

async def check(module: ModuleType, target: str) -> Result:
    module_path = getattr(module, "__file__", "")
    is_email = "email_scan" in module_path

    site_label = get_site_name(module)
    category = find_category(module) or ("Email" if is_email else "Username")

    # Recon requests must remain passive by default. Upstream marks checks
    # that can trigger password-reset or similar notifications as "loud".
    if is_loud(site_label, is_email=is_email):
        return Result.skipped().update(
            site_name=site_label, username=target, category=category, is_email=is_email
        )

    # Some current upstream modules use a shortened validator name (for
    # example ``validate_boot`` in ``boot_dev.py``). Resolve the exported
    # validator instead of assuming it exactly mirrors the filename.
    func = get_scan_func(module)
    if not func:
        return Result.error("Validation function not found").update(
            site_name=site_label, username=target, category=category, is_email=is_email
        )

    try:
        if inspect.iscoroutinefunction(func):
            result = await func(target)
        else:
            loop = asyncio.get_running_loop()
            result = await loop.run_in_executor(_shared_executor, func, target)
    except Exception as e:
        result = Result.error(e)

    return result.update(
        site_name=site_label,
        username=target,
        category=category,
        is_email=is_email
    )


async def check_category(category_name: str, target: str, is_email: bool = True) -> List[Result]:
    categories = load_categories(is_email=is_email)
    cat_path = next((p for name, p in categories.items()
                    if name.lower() == category_name.lower()), None)

    if not cat_path:
        mode = "email_scan" if is_email else "user_scan"
        raise ValueError(f"Category '{category_name}' not found in {mode}")

    modules = load_modules(cat_path)
    tasks = [check(m, target) for m in modules]
    return list(await asyncio.gather(*tasks))


async def check_all(target: str, is_email: bool = True) -> List[Result]:
    categories = load_categories(is_email=is_email)
    results = []

    all_tasks = [check_category(cat_name, target, is_email)
                 for cat_name in categories.keys()]
    nested_results = await asyncio.gather(*all_tasks)

    for sublist in nested_results:
        results.extend(sublist)

    return results


async def check_all_stream(target: str, is_email: bool = True):
    """Yield each completed module result as soon as it settles.

    The framework's streaming endpoint consumes this adapter while retaining
    User Scanner's native ``Result`` object, including its extra and media
    dictionaries.
    """
    categories = load_categories(is_email=is_email)
    modules = [module for path in categories.values() for module in load_modules(path)]
    tasks = [asyncio.create_task(check(module, target)) for module in modules]
    for task in asyncio.as_completed(tasks):
        yield await task
