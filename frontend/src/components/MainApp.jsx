import React, { useEffect, useState } from "react";

//Function HouseList which gathers ALL the data
export default function MainApp() {
  //This sets houses to the [] empty array
  const [houses, setHouses] = useState([]);
  const [loading, setLoading] = useState(true); //This sets "Loading" to true while its loading and sets to false later

  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 20;

  useEffect(() => {
    async function fetchHouses() {
      try {
        const response = await fetch("http://localhost:3000/houses"); // Grabbing response from the server
        const data = await response.json(); //Waiting for the data to be parsed and assigns it to data
        setHouses(data); //Updates houses from earlier with the data
      } catch (error) {
        console.error("error fetching houses: ", error);
      } finally {
        //Finally runs regardless of fail or success.
        setLoading(false);
      }
    }

    fetchHouses();
  }, []);

  if (loading) return <p>Loading houses... </p>;

  //Calculate total pages and house to show
  const totalPages = Math.ceil(houses.length / itemsPerPage);
  const startIndex = (currentPage - 1) * itemsPerPage;
  const currentHouses = houses.slice(startIndex, startIndex + itemsPerPage);

  function nextPage() {
    setCurrentPage((previous) => Math.max(previous + 1, 1));
  }

  function previousPage() {
    setCurrentPage((previous) => Math.max(previous - 1, 1));
  }

  function firstPage() {
    setCurrentPage((previous) => Math.min(previous - 1, 1));
  }

  function lastPage() {
    setCurrentPage(() => Math.max(totalPages));
  }

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
        {currentHouses.map((house) => {
          return (
            <li className="each-house" key={house.id}>
              <img src={house.image} alt="" /> <br />
              Address: {house.address} <br />
              Price: {house.price} <br />
              Type: {house.type}
            </li>
          );
        })}
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
