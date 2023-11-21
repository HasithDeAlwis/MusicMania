import { useState } from "react";
import "./App.css";
import { Button } from "@chakra-ui/react";
import { Route } from "react-router-dom";
import homePage from "./pages/homePage";
import playlistPage from "./pages/playlistPage";
import profilePage from "./pages/profilePage";
import AuthenticationPage from "./pages/AuthenticationPage";

function App() {
  const [count, setCount] = useState(0);

  return (
    <>
      <div className="App">
        <Route path="/home" component={homePage} exact />
        <Route path="/authenticate" component={AuthenticationPage} />
        <Route path="/profile" component={playlistPage} />
        <Route path="/playlist" component={profilePage} />
      </div>
    </>
  );
}

export default App;
