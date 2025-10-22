import Login from "../pages/Login";
import Home_map from "../pages/Home_map";
import Mentions from "../pages/Mentions";
import Sources from "../pages/Sources";
import Characters from "../pages/Characters";
import History from "../pages/History";
import Races from "../pages/Races";
import RaceZoom from "../pages/Race_zoom";

const routes = [
  { path: '/', element: <Home_map /> },
  { path: "/login", element: <Login /> },
  { path: "/Home_map", element: <Home_map /> },
  { path: "/mentions", element: <Mentions />},
  { path: "/sources", element: <Sources />},
  { path: "/characters", element: <Characters />},
  { path: "/histoires", element: <History />},
  { path: "/races", element: <Races />},
  { path: "/races/:id", element: <RaceZoom /> }
]

export default routes;
