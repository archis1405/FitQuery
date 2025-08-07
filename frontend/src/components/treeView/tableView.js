import { useState } from "react";
// Importing Font Awesmome React Component
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"; // Importing FontAwesomeIcon component

// Importing FontAwesome Globally
import { library } from "@fortawesome/fontawesome-svg-core"; // Importing library for FontAwesome icons

// import your icons
import { fab } from "@fortawesome/free-brands-svg-icons"; // Importing FontAwesome brands icons
import { fas } from "@fortawesome/free-solid-svg-icons"; // Importing FontAwesome solid icons
import { far } from "@fortawesome/free-regular-svg-icons"; // Importing FontAwesome regular icons

import { iconMap } from "./icon_map";

library.add(fab, fas, far); // Adding imported icons to the library

export function TableView({ files }) {
  const [expand, setExpand] = useState(false);
  console.log(files);

  return (
    <div>
      <div>
        {files.isFolder ? (
          <button
            className={expand ? "rotate" : ""}
            onClick={() => setExpand(!expand)}
          >
            {" "}
            <FontAwesomeIcon icon="fa-solid fa-angle-right" />
          </button>
        ) : null}{" "}
        <FontAwesomeIcon
          className="file-icon"
          icon={
            files.isDB
              ? iconMap["db"]
              : files.isFolder
              ? iconMap["table"]
              : iconMap["tableColumns"]
          }
          size="xs"
        />
        {files.name}
      </div>

      <div>
        {files.isFolder &&
          expand &&
          files.children.map((exp) => (
            <div style={{ paddingLeft: "40px" }}>
              <TableView files={exp} />
            </div>
          ))}
      </div>
    </div>
  );
}
