export default async function Greeting(){
    const greeting = await fetch("http://localhost:3000/");
    try{
        console.log(greeting);
    }catch (error) {
        console.log(error);
    }
}