import React from "react";
import { connect } from "react-redux";

import Presentation from "./Presentation.js";

import { routes } from "../../../routes";

import { apiReduxApps } from "../../../apiAccess/apiApps";

function AppMenuUnconnected({ children, LOGOUT, logoutStart, authUser }) {
  const [openSlider, setOpenSlider] = React.useState(false);
  const [
    anchorElementProfileMenu,
    setAnchorElementProfileMenu,
  ] = React.useState(null);

  let sliderMenuRoutes = {};
  if (authUser !== undefined) {
    for (const routeName in routes) {
      if (
        routes[routeName].sliderNavigation !== undefined &&
        routes[routeName].show({ authUser })
      ) {
        sliderMenuRoutes[routeName] = routes[routeName];
      }
    }
  }
  function handleOpenSlider() {
    setOpenSlider(true);
  }
  function handleCloseSlider() {
    setOpenSlider(false);
  }

  const handleLogoutClick = () => {
    setAnchorElementProfileMenu(null);
    logoutStart({ callStatus: LOGOUT });
  };

  return (
    <Presentation
      openSlider={openSlider}
      handleOpenSlider={handleOpenSlider}
      handleCloseSlider={handleCloseSlider}
      sliderMenuRoutes={sliderMenuRoutes}
      anchorElementProfileMenu={anchorElementProfileMenu}
      setAnchorElementProfileMenu={setAnchorElementProfileMenu}
      handleLogoutClick={handleLogoutClick}
      authUser={authUser}
    >
      {children}
    </Presentation>
  );
}

const mapStateToProps = (state) => {
  return {
    LOGOUT: state.LOGOUT,
    authUser: state.App.authUser,
  };
};
const mapDispatchToProps = (dispatch) => {
  const logoutStart = ({ callStatus }) => {
    dispatch(apiReduxApps.LOGOUT.operations.start({ callStatus, data: {} }));
  };

  return { logoutStart };
};

const AppMenu = connect(
  mapStateToProps,
  mapDispatchToProps
)(AppMenuUnconnected);

export default AppMenu;
