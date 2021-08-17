import React, {Component} from "react";
import {gql} from '@apollo/client';
import { graphql } from '@apollo/client/react/hoc';
import Typography from '@material-ui/core/Typography';
import {Box, Link} from "@material-ui/core";
import {Link as RouterLink} from "react-router-dom";

const fetchPlanningPeriodById = gql`
    query PlanningPeriodByIdQuery($id: String!) {
        planningPeriodById(id: $id) {
            id 
            name
            
            dedicatedTeams {
                id
                name
            }
        }
    }
`;

class PlanningPeriodDetail extends Component {
    render() {
        if (this.props.data.loading) { return <div>Loading ...</div> }

        const planningPeriodId = this.props.match.params.id
        const planningPeriod = this.props.data.planningPeriodById
        const dedicatedTeams = planningPeriod.dedicatedTeams

        return (
            <Box>
                <Typography variant="h3" noWrap>
                    Выделенные команды
                </Typography>

               <ul>
                    { dedicatedTeams
                        .slice()
                        .sort(function(a, b) {
                            if (a.name > b.name) {
                                return 1;
                            }
                            if (a.name === b.name) {
                                return 0;
                            }
                            if (a.name < b.name) {
                                return -1;
                            }
                        })
                        .map(dedicatedTeam => (
                            <li key={ dedicatedTeam.id }>
                                <RouterLink to={ `/planningPeriods/${planningPeriodId}/dedicatedTeams/${dedicatedTeam.id}` }>
                                { dedicatedTeam.name }
                                </RouterLink>
                            </li>
                        )
                    )}
                </ul>
            </Box>
        );
    }
}

export default graphql(fetchPlanningPeriodById, {
    options: (props) => { return { variables: { id: props.match.params.id }}}
})(PlanningPeriodDetail);