import "./DetailPage.css";
import { useLocation } from "react-router-dom";
import React, { useRef, useState } from "react";
import { PieChart, Pie, Cell } from "recharts";
import Table from "react-bootstrap/Table";
import { Button, Modal } from "react-bootstrap";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faCheck,
  faTriangleExclamation,
} from "@fortawesome/free-solid-svg-icons";

function DetailPage() {
  const { state } = useLocation();
  const HashData = state.data.hash_report[0];
  const vendors = HashData.Processed_Vendor;

  // for modal
  const [show, setShow] = useState(false);

  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);

  // code for auto scroll is provided by
  // https://stackblitz.com/edit/react-ls1dwp?file=index.js
  const myRef = useRef(null);
  const executeScroll = () => myRef.current.scrollIntoView(); // run this function from an event handler or pass it to useEffect to execute scroll

  // code for toggle provided by
  // https://www.codeply.com/p/1NiSJljl0E
  // let [toggle, setToggle] = useState(false);

  // useEffect(() => {
  //   const myCollapse = document.getElementById('vendor_table');
  //   const bsCollapse = new Collapse(myCollapse, {toggle: false});
  //   //toggle ? bsCollapse.show() : bsCollapse.hide()
  // })

  const green_Check = (
    <FontAwesomeIcon icon={faCheck} className="greenInColor" />
  );

  const red_tri_warning = (
    <FontAwesomeIcon icon={faTriangleExclamation} className="redInColor" />
  );

  //console.log(vendors);
  const pieData = [
    { name: "Malicious", value: HashData.NumMalicious },
    { name: "Suspicious", value: HashData.NumSuspicious },
    { name: "Harmless", value: HashData.NumHarmless },
    { name: "Undetected", value: HashData.NumUndetected },
  ];
  const PIECOLOR = ["#fc0303", "#fceb03", "#0367fc", "#808080"];
  const RADIAN = Math.PI / 180;
  const renderCustomizedLabel = ({
    cx,
    cy,
    midAngle,
    innerRadius,
    outerRadius,
    percent,
    index,
  }) => {
    const radius = innerRadius + (outerRadius - innerRadius) * 0.5;
    const x = cx + radius * Math.cos(-midAngle * RADIAN);
    const y = cy + radius * Math.sin(-midAngle * RADIAN);
    if (percent * 100 > 0) {
      return (
        <text
          x={x}
          y={y}
          fill="white"
          textAnchor={x > cx ? "start" : "end"}
          dominantBaseline="central"
        >
          {`${(percent * 100).toFixed(0)}%`}
        </text>
      );
    }
  };
  const TotalVendor =
    HashData.NumHarmless +
    HashData.NumMalicious +
    HashData.NumSuspicious +
    HashData.NumUndetected;
  return (
    <div className="App">
      <header className="App-header" style={{ flexDirection: "column" }}>
        <h1 style={{ marginBottom: 10 }}>Hash: {HashData.Hash}</h1>
        <div
          style={{
            display: "flex",
            flexDirection: "row",
            justifySelf: "space-between",
            fontSize: 20,
          }}
        >
          <h1>Local: {HashData.DateAdded} </h1>
          <h1>VirusTotal: {HashData.DateVT} </h1>
        </div>

        <div style={{ display: "flex", flexDirection: "row" }}>
          <PieChart width={400} height={400}>
            <Pie
              data={pieData}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={renderCustomizedLabel}
              outerRadius={150}
              fill="#8884d8"
              dataKey="value"
            >
              {pieData.map((entry, index) => (
                <Cell
                  key={`cell-${index}`}
                  fill={PIECOLOR[index % PIECOLOR.length]}
                />
              ))}
            </Pie>
          </PieChart>
          <div style={{ fontSize: 15, alignSelf: "center" }}>
            <h1>Malicious: {pieData[0].value}</h1>
            <h1>Suspicious: {pieData[1].value}</h1>
            <h1>Harmless: {pieData[2].value}</h1>
            <h1>Undetected: {pieData[3].value}</h1>
          </div>
        </div>
        <div style={{ fontSize: 15, alignSelf: "center" }}>
          <h3>SHA1: {HashData.SHA1}</h3>
          <h3>SHA256: {HashData.SHA256}</h3>
        </div>
        <div>
          {/*Nav Bar */}
          <div id="Nav Bar" className="container-xl" style={{ paddingTop: 30 }}>
            <nav className="navbar navbar-expand-lg navbar-light bg-light">
              <div className="container-fluid">
                <div
                  className="collapse navbar-collapse"
                  id="navbarNavAltMarkup"
                >
                  <ul className="navbar-nav">
                    <li className="nav-item">
                      <a
                        className="nav-link active"
                        aria-current="page"
                        href="/"
                      >
                        Home
                      </a>
                    </li>

                    <a
                      className="nav-link"
                      onClick={() => {
                        executeScroll(); /*setToggle(toggle => !toggle);*/
                      }}
                      data-toggle="collapse"
                      role="button"
                      aria-expanded="false"
                      aria-controls="vendor_table"
                    >
                      Vendors
                    </a>
                    <a className="nav-link" onClick={handleShow} role="button">
                      Summary
                    </a>
                  </ul>
                </div>
              </div>
            </nav>
          </div>
        </div>
      </header>

      {/*Vendor table*/}
      <div className="container-xl padContainer" ref={myRef}>
        <div id="vendor_table" className="tableFixHead">
          <div className="overflow-scroll">
            <Table className="table table-bordered  table-striped">
              <thead>
                <tr>
                  <th scope="col">Vendor</th>
                  <th scope="col">Result</th>
                </tr>
              </thead>
              <tbody>
                {vendors.map((vendor) => (
                  <tr>
                    <th scope="row" className="col">
                      {vendor.engine_name}
                    </th>
                    {vendor.category === "undetected" ? (
                      <span>
                        {green_Check}
                        <th scope="row" className="col">
                          {vendor.category}
                        </th>
                      </span>
                    ) : vendor.result == null ? (
                      <th scope="row">{vendor.category}</th>
                    ) : (
                      <span>
                        {red_tri_warning}
                        <th scope="row">{vendor.result}</th>
                      </span>
                    )}
                  </tr>
                ))}
              </tbody>
            </Table>
          </div>
        </div>
      </div>
      <div id="Detail_modal" style={{ fontSize: 15 }}>
        <Modal
          size="lg"
          show={show}
          onHide={handleClose}
          backdrop="static"
          keyboard={false}
        >
          <Modal.Header closeButton>
            <Modal.Title>Hash Summary</Modal.Title>
          </Modal.Header>
          <Modal.Body>
            <ul style={{ fontSize: 20 }}>
              <dt>Details</dt>
              <dd>Size: {HashData.Size} bytes</dd>
              <dd>Type: {HashData.Type}</dd>
              <dd>Date Added: {HashData.DateAdded}</dd>
              <dd>VirusTotal Scan Date: {HashData.DateVT}</dd>
              <dd>Lookup Amount: {HashData.Popular} Times</dd>
              <dt>Type of Hashes</dt>
              <dd>md5: {HashData.Hash}</dd>
              <dd>SHA256: {HashData.SHA256}</dd>
              <dd>SHA1: {HashData.SHA1}</dd>
              <dt>Vendor Details</dt>
              <dd>
                Total Number of Vendors:
                {TotalVendor}
              </dd>
              <dd>
                Harmless: {HashData.NumHarmless}/{TotalVendor}
              </dd>
              <dd>
                Suspicious: {HashData.NumSuspicious} /{TotalVendor}
              </dd>
              <dd>
                Malicious: {HashData.NumMalicious}/{TotalVendor}
              </dd>
              <dd>
                Undetected: {HashData.NumUndetected}/{TotalVendor}
              </dd>
            </ul>
          </Modal.Body>
          <Modal.Footer>
            <Button variant="secondary" onClick={handleClose}>
              Close
            </Button>
          </Modal.Footer>
        </Modal>
      </div>
    </div>
  );
}

export default DetailPage;
