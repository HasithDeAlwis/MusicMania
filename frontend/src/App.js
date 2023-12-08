import "./App.css";
import { Route, Switch } from "react-router-dom";
import ProfilePage from "./Pages/ProfilePage";
import SignUpLoginPage from "./Pages/SignUpLoginPage";
import PlaylistPage from "./Pages/PlaylistPage";
import SinglePlaylistPage from "./Pages/SinglePlaylistPage";
import SearchResultsPage from "./Pages/SearchResultsPage";
import logo from "./Assets/Music.png";
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
          <Route path="/user-playlist" component={PlaylistPage} />
          <Route path="/confirmation" component={EmailConfimrationPage} />
          <Route path="/playlist" component={SinglePlaylistPage} />
          <Route path="/search" component={SearchResultsPage} />
        </Switch>
      </div>
    </>
  );
}

export default App;
