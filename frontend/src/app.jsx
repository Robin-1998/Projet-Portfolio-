import Header from './components/header';
import { Routes, Route } from 'react-router-dom';
import BodyAllPage from './components/body_all_page';
import Footer from './components/footer';
import routes from './routes/routes';
import { BrowserRouter } from 'react-router-dom';
import Login from './pages/Login';


function App() {
  return (
    <>
    <BrowserRouter>
      <Header>
        <Routes>
            {/* {routes.map(({ path, element }, index) => (
              <Route key={index} path={path} element={element} />
            ))} */}
        </Routes>
      </Header>
      <BodyAllPage />
      <Footer />
    </BrowserRouter>
    </>
  );
}

export default App
