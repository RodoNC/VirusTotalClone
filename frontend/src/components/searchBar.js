import { FiSearch } from "react-icons/fi";

const SearchBar = ({ searchText, onSearchTextChange, onSubmit }) => {
  // These are passing the data back to HomePage
  const handleSearchTextChange = (event) => {
    onSearchTextChange(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    onSubmit();
  };
  return (
    // Data is at /hashes/xx
    <form
      action="/hashes"
      method="get"
      onSubmit={handleSubmit}
      style={{ justifyItems: "center", display: "flex", flexDirection: "row" }}
    >
      <input
        type="text"
        id="header-search"
        placeholder="Search Hash"
        name="hash"
        onChange={handleSearchTextChange}
        style={{ height: 80, fontSize: 50, paddingRight: 50 }}
      />
      <button
        type="submit"
        style={{
          justifySelf: "center",
          alignItems: "center",
          height: 80,
          fontSize: 50,
        }}
      >
        <FiSearch
          style={{
            justifySelf: "center",
            fontSize: 50,
          }}
        />
      </button>
    </form>
  );
};

export default SearchBar;
