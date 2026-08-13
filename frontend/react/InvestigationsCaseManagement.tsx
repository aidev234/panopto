import {
  Badge,
  Box,
  Button,
  Card,
  CardBody,
  Flex,
  FormControl,
  FormLabel,
  Heading,
  HStack,
  Input,
  Select,
  SimpleGrid,
  Stack,
  Switch,
  Table,
  Tbody,
  Td,
  Text,
  Th,
  Thead,
  Tr,
  VStack,
} from '@chakra-ui/react';
import type { ReactNode } from 'react';

export type InvestigationCase = {
  caseId: string;
  caseName: string;
  status: 'Open' | 'Under Investigation' | 'Closed' | 'Watchlist';
  threatLevel: 'Unassessed' | 'Low Threat' | 'Moderate Threat' | 'Substantial Threat' | 'High Threat' | 'Very High Threat';
  knownLocation?: string;
  openedAt?: string;
  lastEditedAt?: string;
  profileImageUrl?: string;
};

type InvestigationsCaseManagementProps = {
  cases: InvestigationCase[];
  visibleCases: InvestigationCase[];
  searchValue: string;
  statusValue: string;
  threatValue: string;
  sortValue: string;
  onSearchChange: (value: string) => void;
  onStatusChange: (value: string) => void;
  onThreatChange: (value: string) => void;
  onSortChange: (value: string) => void;
  onNewCase: () => void;
  onOpenCase: (caseId: string) => void;
  onEditCase: (caseId: string) => void;
  onDeleteCase: (caseId: string) => void;
  onOpenSettings?: () => void;
};

const threatTone: Record<InvestigationCase['threatLevel'], string> = {
  Unassessed: 'gray',
  'Low Threat': 'green',
  'Moderate Threat': 'yellow',
  'Substantial Threat': 'orange',
  'High Threat': 'red',
  'Very High Threat': 'pink',
};

export function InvestigationsCaseManagement({
  cases,
  visibleCases,
  searchValue,
  statusValue,
  threatValue,
  sortValue,
  onSearchChange,
  onStatusChange,
  onThreatChange,
  onSortChange,
  onNewCase,
  onOpenCase,
  onEditCase,
  onDeleteCase,
  onOpenSettings,
}: InvestigationsCaseManagementProps) {
  const openCases = cases.filter((item) => item.status !== 'Closed').length;
  const watchlistCases = cases.filter((item) => item.status === 'Watchlist').length;

  return (
    <Box as="section" px={{ base: 4, lg: 6 }} py={{ base: 4, lg: 5 }}>
      <Stack spacing={4}>
        <Flex align={{ base: 'stretch', md: 'center' }} justify="space-between" gap={4} direction={{ base: 'column', md: 'row' }}>
          <Box>
            <Text textTransform="uppercase" fontSize="xs" fontWeight="700" letterSpacing=".08em" color="cyan.300">
              Investigations
            </Text>
            <Heading size="lg">Case Management</Heading>
          </Box>
          <HStack spacing={3} align="center" justify="flex-start" flexWrap="wrap" w="full" maxW="48rem">
            <HStack spacing={2} flexWrap="wrap">
              <Metric label="Open Cases" value={openCases} icon="case" />
              <Metric label="Watchlist" value={watchlistCases} icon="shield" />
            </HStack>
            <HStack spacing={2} flexWrap="wrap">
              <Button colorScheme="cyan" onClick={onNewCase}>
                New Case
              </Button>
              {onOpenSettings ? (
                <Button variant="outline" onClick={onOpenSettings}>
                  Settings
                </Button>
              ) : null}
            </HStack>
          </HStack>
        </Flex>

        <Card bg="gray.900" borderWidth="0" borderRadius="md">
          <CardBody p={3}>
            <SimpleGrid columns={{ base: 1, md: 2, xl: 4 }} spacing={3} mb={4}>
              <Input value={searchValue} onChange={(event) => onSearchChange(event.target.value)} placeholder="Search case name or location" />
              <Select value={statusValue} onChange={(event) => onStatusChange(event.target.value)}>
                <option value="">All status</option>
                <option value="Open">Open</option>
                <option value="Under Investigation">Under Investigation</option>
                <option value="Closed">Closed</option>
                <option value="Watchlist">Watchlist</option>
              </Select>
              <Select value={threatValue} onChange={(event) => onThreatChange(event.target.value)}>
                <option value="">All threat levels</option>
                <option value="Unassessed">Unassessed</option>
                <option value="Low Threat">Low Threat</option>
                <option value="Moderate Threat">Moderate Threat</option>
                <option value="Substantial Threat">Substantial Threat</option>
                <option value="High Threat">High Threat</option>
                <option value="Very High Threat">Very High Threat</option>
              </Select>
              <Select value={sortValue} onChange={(event) => onSortChange(event.target.value)}>
                <option value="last_edited_desc">Last edited</option>
                <option value="opened_desc">Opened</option>
                <option value="threat_desc">Threat</option>
                <option value="name_asc">Case name</option>
              </Select>
            </SimpleGrid>

            <VStack align="stretch" spacing={3}>
              {visibleCases.map((item) => (
                <CaseRow key={item.caseId} item={item} onOpenCase={onOpenCase} onEditCase={onEditCase} onDeleteCase={onDeleteCase} />
              ))}
              {!visibleCases.length ? (
                <Box bg="gray.800" borderRadius="md" p={6} textAlign="center" color="gray.400">
                  No matching cases yet.
                </Box>
              ) : null}
            </VStack>
          </CardBody>
        </Card>
      </Stack>
    </Box>
  );
}

function Metric({ label, value, icon }: { label: string; value: number; icon: 'case' | 'shield' }) {
  return (
    <HStack minW="140px" borderWidth="0" borderRadius="md" bg="gray.900" px={3} py={2} spacing={3}>
      <Box boxSize="32px" borderRadius="md" bg="cyan.900" color="cyan.300" display="grid" placeItems="center">
        {icon === 'case' ? <CaseIcon /> : <ShieldIcon />}
      </Box>
      <Box>
        <Text fontSize="xs" color="gray.400" textTransform="uppercase" fontWeight="700" letterSpacing=".08em">
          {label}
        </Text>
        <Text fontSize="xl" fontWeight="800" lineHeight="1">
          {value}
        </Text>
      </Box>
    </HStack>
  );
}

function CaseIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M4 7h16" />
      <path d="M7 7V5h10v2" />
      <path d="M5 7v12h14V7" />
      <path d="M9 12h6" />
    </svg>
  );
}

function ShieldIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M12 3l7 4v5c0 4.5-3 7.5-7 9-4-1.5-7-4.5-7-9V7z" />
      <path d="M9 12l2 2 4-5" />
    </svg>
  );
}

function CaseRow({
  item,
  onOpenCase,
  onEditCase,
  onDeleteCase,
}: {
  item: InvestigationCase;
  onOpenCase: (caseId: string) => void;
  onEditCase: (caseId: string) => void;
  onDeleteCase: (caseId: string) => void;
}) {
  return (
    <Card bg="gray.800" borderWidth="0" borderRadius="md">
      <CardBody p={3}>
        <Flex gap={4} align={{ base: 'stretch', md: 'center' }} direction={{ base: 'column', md: 'row' }}>
          <Box boxSize="64px" borderRadius="md" bg="gray.700" backgroundImage={item.profileImageUrl ? `url(${item.profileImageUrl})` : undefined} backgroundSize="cover" backgroundPosition="center" />
          <Box flex="1" minW={0}>
            <Flex align="baseline" justify="space-between" gap={3}>
              <Heading size="sm" noOfLines={1}>{item.caseName}</Heading>
            </Flex>
            <HStack mt={2} spacing={2} flexWrap="wrap">
              <Badge colorScheme={item.status === 'Closed' ? 'gray' : item.status === 'Watchlist' ? 'purple' : 'cyan'}>{item.status}</Badge>
              <Badge colorScheme={threatTone[item.threatLevel]}>{item.threatLevel}</Badge>
              <Badge bg="gray.700" color="gray.300">{item.knownLocation || 'Unknown'}</Badge>
            </HStack>
            <Text mt={2} fontSize="sm" color="gray.400">
              Last edited {item.lastEditedAt || 'Unknown'}
            </Text>
          </Box>
          <HStack>
            <Button size="sm" colorScheme="cyan" onClick={() => onOpenCase(item.caseId)}>
              Open
            </Button>
            <Button size="sm" variant="ghost" onClick={() => onEditCase(item.caseId)}>
              Edit
            </Button>
            <Button size="sm" variant="ghost" colorScheme="red" onClick={() => onDeleteCase(item.caseId)}>
              Delete
            </Button>
          </HStack>
        </Flex>
      </CardBody>
    </Card>
  );
}

export type EditInvestigationCaseValue = Pick<
  InvestigationCase,
  'caseName' | 'status' | 'threatLevel' | 'knownLocation'
> & {
  retentionPeriod: string;
  monitoringCadence?: string;
  isSecret?: boolean;
};

export type InvestigationAuditLogEntry = {
  queryType: string;
  selector: string;
  user: string;
  dateTime: string;
};

type EditInvestigationCaseFormProps = {
  value: EditInvestigationCaseValue;
  auditLog?: InvestigationAuditLogEntry[];
  onChange: (next: EditInvestigationCaseValue) => void;
  onSubmit: () => void;
  onCancel: () => void;
};

const defaultAuditLog: InvestigationAuditLogEntry[] = [
  { queryType: 'Username Recon', selector: '@mason_hale', user: 'john@isb.com', dateTime: '29 May 2026, 01:42 UTC' },
  { queryType: 'Email Enrichment', selector: 'm.hale@example.com', user: 'john@isb.com', dateTime: '29 May 2026, 01:37 UTC' },
  { queryType: 'Phone Lookup', selector: '+1 202 555 0147', user: 'john@isb.com', dateTime: '29 May 2026, 01:31 UTC' },
];

export function EditInvestigationCaseForm({ value, auditLog = defaultAuditLog, onChange, onSubmit, onCancel }: EditInvestigationCaseFormProps) {
  const update = (patch: Partial<EditInvestigationCaseValue>) => onChange({ ...value, ...patch });

  return (
    <Box bg="gray.900" borderRadius="lg" p={4}>
      <Flex justify="space-between" align="flex-start" gap={4} mb={4}>
        <Box>
          <Text textTransform="uppercase" fontSize="xs" fontWeight="700" letterSpacing=".08em" color="cyan.300">
            Investigations
          </Text>
          <Heading size="md">Case Settings</Heading>
        </Box>
        <Button variant="ghost" onClick={onCancel}>Close</Button>
      </Flex>

      <Stack spacing={3}>
        <Box bg="cyan.900" borderRadius="md" p={3}>
          <SectionLabel>Identity</SectionLabel>
          <SimpleGrid columns={{ base: 1, md: 2 }} spacing={3} mt={2}>
            <FormControl>
              <FormLabel color="gray.400">Case Title</FormLabel>
              <Input value={value.caseName} onChange={(event) => update({ caseName: event.target.value })} bg="blackAlpha.400" borderWidth="0" />
            </FormControl>
            <FormControl>
              <FormLabel color="gray.400">Known Location</FormLabel>
              <Input value={value.knownLocation || ''} onChange={(event) => update({ knownLocation: event.target.value })} bg="blackAlpha.400" borderWidth="0" />
            </FormControl>
          </SimpleGrid>
        </Box>

        <Box bg="gray.800" borderRadius="md" p={3}>
          <SectionLabel>Status & Risk</SectionLabel>
          <SimpleGrid columns={{ base: 1, md: 2 }} spacing={3} mt={2}>
            <FormControl>
              <FormLabel color="gray.400">Status</FormLabel>
              <Select value={value.status} onChange={(event) => update({ status: event.target.value as InvestigationCase['status'] })} bg="blackAlpha.400" borderWidth="0">
                <option value="Open">Open</option>
                <option value="Under Investigation">Under Investigation</option>
                <option value="Closed">Closed</option>
                <option value="Watchlist">Watchlist</option>
              </Select>
            </FormControl>
            <FormControl>
              <FormLabel color="gray.400">Threat Level</FormLabel>
              <Select value={value.threatLevel} onChange={(event) => update({ threatLevel: event.target.value as InvestigationCase['threatLevel'] })} bg="blackAlpha.400" borderWidth="0">
                <option value="Unassessed">Unassessed</option>
                <option value="Low Threat">Low Threat</option>
                <option value="Moderate Threat">Moderate Threat</option>
                <option value="Substantial Threat">Substantial Threat</option>
                <option value="High Threat">High Threat</option>
                <option value="Very High Threat">Very High Threat</option>
              </Select>
            </FormControl>
            {value.status === 'Watchlist' ? (
              <FormControl>
                <FormLabel color="gray.400">Monitoring Refresh Cadence</FormLabel>
                <Input value={value.monitoringCadence || ''} onChange={(event) => update({ monitoringCadence: event.target.value })} bg="blackAlpha.400" borderWidth="0" />
              </FormControl>
            ) : null}
            <FormControl>
              <FormLabel color="gray.400">Data Retention Period</FormLabel>
              <Select value={value.retentionPeriod} onChange={(event) => update({ retentionPeriod: event.target.value })} bg="blackAlpha.400" borderWidth="0">
                <option value="24h">24h</option>
                <option value="1 week">1 week</option>
                <option value="3 week">3 week</option>
                <option value="6 weeks">6 weeks</option>
                <option value="3 months">3 months</option>
                <option value="1 year">1 year</option>
              </Select>
            </FormControl>
          </SimpleGrid>
        </Box>

        <Box bg="gray.800" borderRadius="md" p={3}>
          <SectionLabel>Privacy</SectionLabel>
          <HStack mt={3} justify="space-between" align="center">
            <Box>
              <Text fontWeight="700">Secret Case</Text>
              <Text fontSize="sm" color="gray.400">Restrict case visibility and handling.</Text>
            </Box>
            <Switch colorScheme="cyan" isChecked={value.isSecret === true} onChange={(event) => update({ isSecret: event.target.checked })} />
          </HStack>
        </Box>

        <Box bg="gray.800" borderRadius="md" p={3}>
          <Flex justify="space-between" align="center" gap={3}>
            <SectionLabel>Investigation Audit Log</SectionLabel>
            <Text fontSize="xs" color="gray.400">Example Activity</Text>
          </Flex>
          <Table size="sm" variant="unstyled" mt={3}>
            <Thead>
              <Tr>
                <Th color="gray.400" px={2}>Query Type</Th>
                <Th color="gray.400" px={2}>Selector</Th>
                <Th color="gray.400" px={2}>User</Th>
                <Th color="gray.400" px={2}>Date / Time</Th>
              </Tr>
            </Thead>
            <Tbody>
              {auditLog.map((entry) => (
                <Tr key={`${entry.queryType}-${entry.selector}-${entry.dateTime}`} bg="blackAlpha.300">
                  <Td px={2}>{entry.queryType}</Td>
                  <Td px={2}>{entry.selector}</Td>
                  <Td px={2}>{entry.user}</Td>
                  <Td px={2}>{entry.dateTime}</Td>
                </Tr>
              ))}
            </Tbody>
          </Table>
        </Box>

        <HStack justify="flex-end" bg="blackAlpha.400" borderRadius="md" p={3}>
          <Button colorScheme="cyan" onClick={onSubmit}>Save Changes</Button>
          <Button variant="ghost" onClick={onCancel}>Cancel</Button>
        </HStack>
      </Stack>
    </Box>
  );
}

function SectionLabel({ children }: { children: ReactNode }) {
  return (
    <Text textTransform="uppercase" fontSize="xs" fontWeight="800" letterSpacing=".08em" color="cyan.300">
      {children}
    </Text>
  );
}
