import React, { useState, useEffect } from "react";
import { Inter } from "next/font/google";
import {
  Tabs,
  Tab,
  Box,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  TextField,
  Button,
  CircularProgress,
} from "@mui/material";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import Paper from "@mui/material/Paper";
import {
  STATE_ABBREVIATIONS,
  STATE_FIPS_CODES,
  LOCATION_TYPES,
  REGIONS,
} from "@/config/constants";
import { useMutation } from "@tanstack/react-query";
import { SelectChangeEvent } from "@mui/material";
import { CSVLink } from "react-csv";

const inter = Inter({ subsets: ["latin"] });

interface Props {
  data: any;
}
interface SearchParams {
  query: string;
  locationType: string;
  region: string;
  stateAbbreviation: string;
  stateFipsCode: string;
  parclId: number | null;
  geoid: string;
  sortBy: string;
  sortOrder: string;
  limit: number;
  offset: number;
}
interface Item {
  parcl_id: number;
  country: string;
  geoid: string;
  state_fips_code: string | null;
  name: string;
  state_abbreviation: string | null;
  region: string | null;
  location_type: string;
  total_population: number;
  median_income: number;
  parcl_exchange_market: number;
  pricefeed_market: number;
  case_shiller_10_market: number;
  case_shiller_20_market: number;
}

interface FetchDataMutationResult {
  items: Item[];
  total: number;
  limit: number;
  offset: number;
  links: {
    first: string;
    last: string;
    self: string;
    next: string | null;
    prev: string | null;
  };
}

type FetchDataError = Error;

const fetcher = async (url: string) => {
  const response = await fetch(url, {
    headers: {
      Authorization: `${process.env.NEXT_PUBLIC_PARCLLABS_API_KEY}`,
      Accept: "application/json",
    },
  });
  if (!response.ok) {
    throw new Error("Network response was not ok");
  }
  return response.json();
};

const buildQueryString = (params: SearchParams) => {
  const queryParams: Record<string, string> = {};
  if (params.query) queryParams.query = params.query;
  if (params.locationType) queryParams.location_type = params.locationType;
  if (params.region) queryParams.region = params.region;
  if (params.stateAbbreviation)
    queryParams.state_abbreviation = params.stateAbbreviation;
  if (params.stateFipsCode) queryParams.state_fips_code = params.stateFipsCode;
  if (params.parclId !== null) queryParams.parcl_id = params.parclId.toString();
  if (params.geoid) queryParams.geoid = params.geoid;
  if (params.sortBy) queryParams.sort_by = params.sortBy;
  if (params.sortOrder) queryParams.sort_order = params.sortOrder;
  queryParams.limit = params.limit.toString();
  queryParams.offset = params.offset.toString();

  return new URLSearchParams(queryParams).toString();
};

export default function Home({ data }: Props) {
  const [searchParams, setSearchParams] = useState<SearchParams>({
    query: "",
    locationType: "",
    region: "",
    stateAbbreviation: "",
    stateFipsCode: "",
    parclId: null,
    geoid: "",
    sortBy: "",
    sortOrder: "",
    limit: 12,
    offset: 0,
  });

  const [queryString, setQueryString] = useState<string>("");
  const [tabIndex, setTabIndex] = useState(0);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>): void => {
    const { name, value } = e.target;
    setSearchParams((prevParams) => ({
      ...prevParams,
      [name]: value,
    }));
  };

  const handleSelectChange = (e: SelectChangeEvent<string>): void => {
    const { name, value } = e.target;
    setSearchParams((prevParams) => ({
      ...prevParams,
      [name]: value,
    }));
  };
  const handleFetchData = () => {
    const newQueryString = buildQueryString(searchParams);
    setQueryString(newQueryString);
    fetchDataMutation.mutate(newQueryString); // Trigger mutation with updated query string
  };

  const fetchDataMutation = useMutation<
    FetchDataMutationResult,
    FetchDataError,
    string
  >({
    mutationFn: async (queryString: string) => {
      const data = await fetcher(`/api/proxy?${queryString}`);
      return data;
    },
    onSuccess: (data) => {
      console.log("Data fetched successfully:", data);
    },
    onSettled: () => {
      setTabIndex(1);
    },
    onError: (error) => {
      console.error("Error:", error);
    },
  });

  useEffect(() => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  }, [tabIndex]);

  if (fetchDataMutation.isPending) {
    return (
      <div className="loading-overlay">
        <CircularProgress />
      </div>
    );
  }
  if (fetchDataMutation.isError) return <div>Failed to load data</div>;

  return (
    <main
      className={`flex min-h-screen flex-col items-center justify-between p-24 ${inter.className}`}
    >
      <Box
        sx={{
          width: "100%",
          maxWidth: 1000,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
        }}
      >
        <Tabs
          value={tabIndex}
          onChange={(e, newValue) => setTabIndex(newValue)}
          aria-label="basic tabs example"
        >
          <Tab label="Search" />
          <Tab label="Results" />
        </Tabs>
        <TabPanel value={tabIndex} index={0}>
          <div className="form-container">
            <form className="space-y-6 p-6 bg-white rounded-lg shadow-lg">
              <div className="w-full">
                <TextField
                  fullWidth
                  label="Search Query"
                  name="query"
                  value={searchParams.query}
                  onChange={handleInputChange}
                  placeholder="Ex: New York"
                />
              </div>
              <div className="w-full">
                <TextField
                  fullWidth
                  label="Geographic Identifier (GEOID)"
                  name="geoid"
                  value={searchParams.geoid}
                  onChange={handleInputChange}
                />
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <FormControl fullWidth>
                  <InputLabel>Location Type</InputLabel>
                  <Select
                    name="locationType"
                    value={searchParams.locationType}
                    onChange={handleSelectChange}
                  >
                    {LOCATION_TYPES.map((type) => (
                      <MenuItem key={type} value={type}>
                        {type}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
                <FormControl fullWidth>
                  <InputLabel>Region</InputLabel>
                  <Select
                    name="region"
                    value={searchParams.region}
                    onChange={handleSelectChange}
                  >
                    {REGIONS.map((region) => (
                      <MenuItem key={region} value={region}>
                        {region.replace("_", " ")}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
                <FormControl fullWidth>
                  <InputLabel>State Abbreviation</InputLabel>
                  <Select
                    name="stateAbbreviation"
                    value={searchParams.stateAbbreviation}
                    onChange={handleSelectChange}
                  >
                    {STATE_ABBREVIATIONS.map((abbreviation) => (
                      <MenuItem key={abbreviation} value={abbreviation}>
                        {abbreviation}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
                <FormControl fullWidth>
                  <InputLabel>State FIPS Code</InputLabel>
                  <Select
                    name="stateFipsCode"
                    value={searchParams.stateFipsCode}
                    onChange={handleSelectChange}
                  >
                    {STATE_FIPS_CODES.map((code) => (
                      <MenuItem key={code} value={code}>
                        {code}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
                <FormControl fullWidth>
                  <InputLabel>Sort By</InputLabel>
                  <Select
                    name="sortBy"
                    value={searchParams.sortBy}
                    onChange={handleSelectChange}
                  >
                    <MenuItem value="TOTAL_POPULATION">
                      Total Population
                    </MenuItem>
                    <MenuItem value="PRICE_DROP">Price Drop</MenuItem>
                  </Select>
                </FormControl>
                <FormControl fullWidth>
                  <InputLabel>Sort Order</InputLabel>
                  <Select
                    name="sortOrder"
                    value={searchParams.sortOrder}
                    onChange={handleSelectChange}
                  >
                    <MenuItem value="ASC">Ascending</MenuItem>
                    <MenuItem value="DESC">Descending</MenuItem>
                  </Select>
                </FormControl>
                <TextField
                  fullWidth
                  type="number"
                  label="Limit"
                  name="limit"
                  value={searchParams.limit}
                  onChange={handleInputChange}
                  inputProps={{ min: 1, max: 1000 }}
                />
                <TextField
                  fullWidth
                  type="number"
                  label="Offset"
                  name="offset"
                  value={searchParams.offset}
                  onChange={handleInputChange}
                  inputProps={{ min: 0, max: 1000 }}
                />
              </div>
              <div className="w-full">
                <Button
                  variant="contained"
                  color="primary"
                  onClick={handleFetchData}
                  className="w-full py-3 text-lg"
                >
                  Fetch Data
                </Button>
              </div>
            </form>
          </div>
        </TabPanel>
        <TabPanel value={tabIndex} index={1}>
          {fetchDataMutation.isSuccess && (
            <>
              <TableContainer className="table-container" component={Paper}>
                <Table
                  sx={{ minWidth: 650 }}
                  size="small"
                  aria-label="a dense table"
                >
                  <TableHead>
                    <TableRow>
                      <TableCell className="text-xs" align="left">
                        parcl_id
                      </TableCell>
                      <TableCell className="text-xs" align="left">
                        country
                      </TableCell>
                      <TableCell className="text-xs" align="left">
                        state_fips_code
                      </TableCell>
                      <TableCell className="text-xs" align="left">
                        geoid
                      </TableCell>
                      <TableCell className="text-xs" align="left">
                        name
                      </TableCell>
                      <TableCell className="text-xs" align="left">
                        state_abbreviation
                      </TableCell>
                      <TableCell className="text-xs" align="left">
                        region
                      </TableCell>
                      <TableCell className="text-xs" align="left">
                        location_type
                      </TableCell>
                      <TableCell className="text-xs" align="left">
                        total_population
                      </TableCell>
                      <TableCell className="text-xs" align="left">
                        median_income
                      </TableCell>
                      <TableCell className="text-xs" align="left">
                        parcl_exchange_market
                      </TableCell>
                      <TableCell className="text-xs" align="left">
                        pricefeed_market
                      </TableCell>
                      <TableCell className="text-xs" align="left">
                        case_shiller_10_market
                      </TableCell>
                      <TableCell className="text-xs" align="left">
                        case_shiller_20_market
                      </TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {fetchDataMutation.data.items.map((row) => (
                      <TableRow
                        key={row.parcl_id}
                        // sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                      >
                        <TableCell
                          className="text-xs"
                          align="left"
                          component="th"
                          scope="row"
                        >
                          {row.parcl_id}
                        </TableCell>
                        <TableCell className="text-xs" align="left">
                          {row.country}
                        </TableCell>
                        <TableCell className="text-xs" align="left">
                          {row.geoid}
                        </TableCell>
                        <TableCell className="text-xs" align="left">
                          {row.state_fips_code}
                        </TableCell>
                        <TableCell className="text-xs" align="left">
                          {row.name}
                        </TableCell>
                        <TableCell className="text-xs" align="left">
                          {row.state_abbreviation}
                        </TableCell>
                        <TableCell className="text-xs" align="left">
                          {row.region}
                        </TableCell>
                        <TableCell className="text-xs" align="left">
                          {row.location_type}
                        </TableCell>
                        <TableCell className="text-xs" align="left">
                          {row.total_population}
                        </TableCell>
                        <TableCell className="text-xs" align="left">
                          {row.median_income}
                        </TableCell>
                        <TableCell className="text-xs" align="left">
                          {row.parcl_exchange_market}
                        </TableCell>
                        <TableCell className="text-xs" align="left">
                          {row.pricefeed_market}
                        </TableCell>
                        <TableCell className="text-xs" align="left">
                          {row.case_shiller_10_market}
                        </TableCell>
                        <TableCell className="text-xs" align="left">
                          {row.case_shiller_20_market}
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
              <div className="export-button-container">
                <CSVLink
                  data={fetchDataMutation.data.items}
                  filename={"my-data.csv"}
                  className="w-72 py-3 text-lg m-auto export-button "
                >
                  EXPORT DATA TO CSV
                </CSVLink>
              </div>
            </>
          )}
        </TabPanel>
      </Box>
    </main>
  );
}

function TabPanel(props: {
  children?: React.ReactNode;
  index: number;
  value: number;
}) {
  const { children, value, index } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`tab-panel-${index}`}
      aria-labelledby={`tab-${index}`}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}
