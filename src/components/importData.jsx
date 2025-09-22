import React, {useEffect, useState} from "react";

//Function HouseList which gathers ALL the data
function HouseList() {
    //This sets houses to the [] empty array
    //And is uses the function setHouses LATER to update the array!? cool!
    const [houses, setHouses] = useState([]);
    const [loading, setLoading] = useState(true); //This sets "Loading" to true while its loading and sets to false later

    useEffect(() => {
        async function fetchHouses(){
            try{
                const response = await fetch('http://localhost:3000/houses'); // Grabbing response from the server
                const data = await response.json(); //Waiting for the data to be parsed and assigns it to data
                setHouses(data); //Updates houses from earlier with the data
            }catch (error) {
                console.error("error fetching houses: ", error);
            }finally { //Finally runs regardless of fail or success.
                setLoading(false);
            }
        };

        fetchHouses();
    }, []);

    if (loading) return <p>Loading houses... </p>;

    return (
        <div className="houses-card">
            <ul>
                {houses.map((house, index) => {
                    return (
                        <li className="each-house" key={index}>
                            <img src={house.image} alt="" /> <br />
                            Address: {house.address} <br/>
                            Price: {house.price} <br />
                            Type: {house.type}
                        </li>
                )})}
            </ul>
        </div>
    );
};

export default HouseList;