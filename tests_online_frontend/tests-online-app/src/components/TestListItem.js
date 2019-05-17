import React, {Component} from "react";
import {connect} from "react-redux";
import {withRouter} from "react-router-dom"
import * as ui from "semantic-ui-react";

import styles from "./TestListItem.module.css"

const mapStateToProps = state => {
    return {user: state.api_user_info.data.username}
};

class ConnectedTestListItem extends Component {
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

    handleEditClick = e => {
        e.preventDefault();
        e.stopPropagation();
    };

    handleStatClick = e => {
        e.preventDefault();
        e.stopPropagation();
    };

    render() {
        return <ui.Card
            raised={this.state.isHovered}
            href='#'
            onClick={this.handleClick}
            onMouseEnter={this.onMouseEnter}
            onMouseLeave={this.onMouseLeave}
            className={styles.card}
        >
            <ui.Card.Content>
                <ui.Card.Header style={{
                    display: "flex",
                    alignItems: "flex-start"
                }}>
                    {this.props.title}
                    &nbsp;
                    <ui.Popup className={styles.smallLabel} position='top right' size="mini" inverted
                              content='Questions number'
                              trigger={
                                  this.props.user_answers ?
                                      <ui.Label className={styles.smallLabel}
                                                color={this.props.user_answers === this.props.questions_number
                                                    ? "green" : "olive"
                                                }>
                                          {this.props.user_answers}/{this.props.questions_number}
                                      </ui.Label>
                                      :
                                      <ui.Label className={styles.smallLabel}>
                                          {this.props.questions_number}
                                      </ui.Label>
                              }
                    />
                </ui.Card.Header>
                <ui.Card.Description>
                    {((s, cut) => s.length > cut ? s.slice(0, cut) + '...' : s)(
                        this.props.description, this.props.descriptionCut
                    )}
                </ui.Card.Description>
            </ui.Card.Content>
            <div className={styles.buttonGroup + " not-implemented"}>
                {this.props.owner === this.props.user &&
                <div style={{marginBottom: ".2em"}}>
                    <ui.Button animated='vertical' size="small" onClick={this.handleEditClick}>
                        <ui.Button.Content hidden>Edit</ui.Button.Content>
                        <ui.Button.Content visible className={styles.iconBtn}>
                            <ui.Icon name="edit"/>
                        </ui.Button.Content>
                    </ui.Button>
                </div>
                }
                <div>
                    <ui.Button animated='vertical' size="small" onClick={this.handleStatClick}>
                        <ui.Button.Content hidden>Stats</ui.Button.Content>
                        <ui.Button.Content visible className={styles.iconBtn}>
                            <ui.Icon name="area graph"/>
                        </ui.Button.Content>
                    </ui.Button>
                </div>
            </div>
            <div className={styles.author}>{this.props.owner}</div>
        </ui.Card>;
    }
}

ConnectedTestListItem.defaultProps = {
    descriptionCut: 200
};

export default withRouter(connect(mapStateToProps)(ConnectedTestListItem));