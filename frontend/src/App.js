import "./App.css";
import { Route, Switch } from "react-router-dom";
import ProfilePage from "./Pages/ProfilePage";
import SignUpLoginPage from "./Pages/SignUpLoginPage";
import PlaylistPage from "./Pages/PlaylistPage";
import logo from "./Assets/Music.png"
import NavigationBar from "./Components/NavigationBar";
import EmailConfimrationPage from "./Pages/EmailConfimrationPage";
function App() {

  return (
    <>
      <NavigationBar />
      <div className="App">
        <Switch>
          <Route path="/authenticate" component={SignUpLoginPage} exact />
          <Route path="/profile" component={ProfilePage} />
          <Route path="/playlist" component={PlaylistPage} />
          <Route path="/confirmation" component={EmailConfimrationPage} />
        </Switch>
        
      </div>
    </>
  );
}

export default App;