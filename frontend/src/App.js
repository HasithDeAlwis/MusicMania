import "./App.css";
import { Route } from "react-router-dom";
import ProfilePage from "./Pages/ProfilePage";
import SignUpLoginPage from "./Pages/SignUpLoginPage";
import PlaylistPage from "./Pages/PlaylistPage";
import logo from "./Assets/Music.png"
import NavigationBar from "./Components/NavigationBar";
function App() {

  return (
    <>
      <NavigationBar />
      <div className="App">
        <Route path="/authenticate" component={SignUpLoginPage} />
        <Route path="/profile" component={ProfilePage} exact/>
        <Route path="/playlist" component={PlaylistPage} />
      </div>
    </>
  );
}

export default App;