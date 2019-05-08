import React, {Component} from "react";
import Auth from "./Auth";

import TestsList from "./presentation/TestsList";

export class App extends Component {
    render() {
        return (
            <div id="app-root">
                <Auth/>
                <TestsList/>
            </div>
        );
    }
}

export default App;