// import React, { useState, useEffect } from 'react';

import { TableView } from "./treeView/tableView";
import { files } from "./treeView/data";
const Sidebar = ({ tables }) => {
  return (
    <div className="sidebar">
      <h4>Database Tables</h4>
      <TableView files={files} />
    </div>
  );
};

export default Sidebar;
