import Login from "../pages/Login";
import Home from "../pages/Home";
import Home_map from "../pages/Home_map";

const routes = [
	{ path: "/", element : <Home />},
	{ path: "/login", element: <Login /> },
	{ path: "/Home_map", element: <Home_map /> }
]

export default routes
