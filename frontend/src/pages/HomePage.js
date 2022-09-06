import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import axios from "axios";

import "./HomePage.css";
import HistoryBox from "../components/historyBox";
import SearchBar from "../components/searchBar";
import PopularBox from "../components/popularBox";

function HomePage() {
  const navigate = useNavigate();
  const [search, setSearch] = useState(""); //Hashes in form of String
  const [Popular, setPopular] = useState([]); // List of Popular Hashes
  const [History, setHistory] = useState([]); // List of Historic Hashes

  function refreshPage() {
    window.location.reload(false);
  }
  useEffect(() => {
    const extraPath = "http://127.0.0.1:5000/extra";
    axios.get(extraPath).then((resp) => {
      setHistory(resp.data["db_report"][0]["Date"]);
      setPopular(resp.data["db_report"][0]["Popular"]);
    });
  }, []);
  console.log(History);
  console.log(Popular);
  // This method handles search form (POST request to backend, and handles response)
  const handleFormSubmit = (Event) => {
    // HASH is located in search
    const path = "http://127.0.0.1:5000/hashes";
    let payload = {
      Hash: search,
    };
    axios
      .post(path, payload)
      .then((resp) => {
        // Handle response from backend
        //console.log(resp.data);
        navigate(`${search}`, {
          state: {
            data: resp.data,
          },
        }); // TEST: navigating to the details page.
      })
      .catch((error) => {
        // Handle error
        navigate("/");
        refreshPage();
        alert("ERROR: Invalid Hash || General ERROR");
        console.log(error);
      });
  };

  // This gets the data from whatever the user enters and sets its state
  const inputHandler = (Event) => {
    setSearch(Event);
  };

  return (
    <div className="App">
      <header className="App-header" style={{ flexDirection: "column" }}>
        <h1 style={{ fontSize: 75 }}>Virus Lookup </h1>
        <SearchBar
          searchText={search}
          onSearchTextChange={inputHandler}
          onSubmit={handleFormSubmit}
        />
        <div style={{ display: "flex", flexDirection: "row" }}>
          <HistoryBox data={History} />
          <PopularBox data={Popular} />
        </div>
      </header>
    </div>
  );
}

export default HomePage;
