import { all } from "redux-saga/effects";

import { authSagas as googleSagas } from "../utils/googleLogin";

import { apiReduxWatchers } from "../apiAccess/apiApps";
import { appSagas } from "../components/App/redux";
import { agileBoardSagas } from "../components/regions/AgileBoard/redux";
import { cardDetailsSagas } from "../components/regions/CardDetails/redux";

import { addCardReviewSagas } from "../components/regions/AddCardReviewModal/redux";

// import { markSingleCardWorkshopAttendanceSagas } from "../components/regions/MarkSingleCardAttendanceModal/redux";

// import { entitiesSagas } from "../apiAccess/redux";

import { apiReduxWatchers as coreApiReduxWatchers } from "@prelude/redux-api-toolbox/src/djRestAuth";
import { utilitySagas } from "@prelude/redux-api-toolbox/src/utilities";

export function* rootSaga() {
  yield all([
    ...googleSagas,
    ...apiReduxWatchers,
    // ...entitiesSagas,
    ...appSagas,
    ...agileBoardSagas,
    ...cardDetailsSagas,
    ...addCardReviewSagas,
    // ...markSingleCardWorkshopAttendanceSagas,
    ...coreApiReduxWatchers,
    ...utilitySagas,
  ]);
}
