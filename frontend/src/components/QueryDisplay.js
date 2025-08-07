import React from "react";
import { DataGrid } from "@mui/x-data-grid";
import { Box } from "@mui/material";
import "./QueryDisplay.css"; // Ensure you import your CSS file

const QueryDisplay = ({ query, result }) => {
  // Add a null check for result and default it to an empty array if it's null or undefined
  const hasResult = result && result.length > 0;

  // Prepare columns and rows for DataGrid if there is a valid result
  const columns = hasResult
    ? Object.keys(result[0]).map((key) => ({
        field: key,
        headerName: key,
        width: 150,
      }))
    : [];

  const rows = hasResult
    ? result.map((row, index) => ({
        id: row.id || index, // Ensure each row has an `id` field
        ...row,
      }))
    : [];

  return (
    <div className="query-display">
      {/* Display the SQL query */}
      {query && (
        <div className="query-section">
          <h4>Generated SQL Query:</h4>
          <pre>{query}</pre>
        </div>
      )}

      {/* Display a message if no results */}
      {!hasResult && (
        <div className="no-results">
          <h4>No results found</h4>
        </div>
      )}

      {/* Display the fetched data using DataGrid */}
      {hasResult && (
        <div className="result-section">
          <Box className="custom-datagrid">
            <DataGrid
              rows={rows}
              columns={columns}
              pageSize={5}
              rowsPerPageOptions={[5]}
              pagination
            />
          </Box>
        </div>
      )}
    </div>
  );
};

export default QueryDisplay;
