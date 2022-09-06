import React from "react";
import Table from "react-bootstrap/Table";

const HistoryBox = ({ data }) => {
  return (
    <div
      style={{
        padding: "20px",
      }}
    >
      <Table
        className="table table-bordered  table-striped"
        style={{
          backgroundColor: "White",
          borderColor: "black",
        }}
      >
        <thead>
          <tr>
            <th scope="col">md5 Hash</th>
            <th scope="col">Date Added</th>
          </tr>
        </thead>
        <tbody>
          {data.map((hash) => (
            <tr>
              <th scope="row" className="col" style={{ fontSize: 25 }}>
                {hash[0]}
              </th>
              <th scope="row" className="col">
                {hash[1]}
              </th>
            </tr>
          ))}
        </tbody>
      </Table>
    </div>
  );
};

export default HistoryBox;
