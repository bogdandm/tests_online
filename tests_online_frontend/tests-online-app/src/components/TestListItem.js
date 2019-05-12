import React, {Component} from "react";
import {withRouter} from "react-router-dom"
import * as ui from "semantic-ui-react";

import styles from "./TestListItem.module.css"

class TestListItem extends Component {
    state = {
        isHovered: false,
    };

    onMouseEnter = () => {
        this.setState({isHovered: true});
    };

    onMouseLeave = () => {
        this.setState({isHovered: false});
    };

    handleClick = e => {
        const history = this.props.history;
        history.push(`/test/${this.props.hash}`);
        e.preventDefault()
    };

    render() {
        return <ui.Card
            raised={this.state.isHovered}
            href='#'
            onClick={this.handleClick}
            onMouseEnter={this.onMouseEnter}
            onMouseLeave={this.onMouseLeave}
            style={{
                color: "inherit",
                paddingRight: 50
            }}
        >
            <ui.Card.Content
                header={this.props.title}
                description={
                    ((s, cut) => s.length > cut ? s.slice(0, cut) + '...' : s)
                    (this.props.description, this.props.descriptionCut)
                }
            />
            <div className={styles.buttonGroup}>1234</div>
            <div className={styles.author}>{this.props.owner}</div>
        </ui.Card>;
    }
}

TestListItem.defaultProps = {
    descriptionCut: 200
};

export default withRouter(TestListItem);