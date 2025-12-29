import React, { useEffect, useState } from "react";
import axios from "axios";

// Function HouseList which gathers ALL the data
export default function MainApp() {
  // State
  const [houses, setHouses] = useState([]);
  const [loading, setLoading] = useState(true);

  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 20;

  useEffect(() => {
    async function fetchHouses() {
      try {
        const response = await axios.get("http://localhost:3000/houses");
        console.log(response.data);
        setHouses(response.data);
      } catch (error) {
        console.error("error fetching houses:", error);
      } finally {
        setLoading(false);
      }
    }

    fetchHouses();
  }, []);

  if (loading) return <p>Loading houses...</p>;

  // Pagination calculations
  const totalPages = Math.ceil(houses.length / itemsPerPage);
  const startIndex = (currentPage - 1) * itemsPerPage;
  const currentHouses = houses.slice(startIndex, startIndex + itemsPerPage);

  //Pagination functions
  function nextPage() {
    setCurrentPage((prev) => Math.min(prev + 1, totalPages));
  }

  function previousPage() {
    setCurrentPage((prev) => Math.max(prev - 1, 1));
  }

  function firstPage() {
    setCurrentPage(1);
  }

  function lastPage() {
    setCurrentPage(totalPages);
  }

  //Export
  return (
    <div className="houses-card">
      <div className="pagination">
        <button onClick={firstPage} disabled={currentPage === 1}>
          First
        </button>
        <button onClick={previousPage} disabled={currentPage === 1}>
          Back
        </button>
        <span>
          Page {currentPage} of {totalPages}
        </span>
        <button onClick={nextPage} disabled={currentPage === totalPages}>
          Next
        </button>
        <button onClick={lastPage} disabled={currentPage === totalPages}>
          Last
        </button>
      </div>

      <ul>
        {currentHouses.map((house) => (
          <li className="each-house" key={house.id}>
            <img src={house.image} alt={house.address} />
            <br />
            Address: {house.address}
            <br />
            Price: {house.price}
            <br />
            Type: {house.type}
          </li>
        ))}
      </ul>

      <div className="pagination">
        <button onClick={previousPage} disabled={currentPage === 1}>
          Back
        </button>
        <span>
          Page {currentPage} of {totalPages}
        </span>
        <button onClick={nextPage} disabled={currentPage === totalPages}>
          Next
        </button>
      </div>
    </div>
  );
}
