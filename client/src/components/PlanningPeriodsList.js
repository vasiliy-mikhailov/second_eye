import React, {Component} from "react";
import {gql} from '@apollo/client';
import { graphql } from '@apollo/client/react/hoc';
import Typography from '@material-ui/core/Typography';
import {Box} from "@material-ui/core";
import {Link as RouterLink} from "react-router-dom";

const fetchPlanningPeriods = gql`
    query PlanningPeriods {
        planningPeriods {
            id 
            name
            start
            end
        }
    }
`;

class PlanningPeriodsList extends Component {
    render() {
        if (this.props.data.loading) { return <div>Loading ...</div> }

        const planningPeriods = this.props.data.planningPeriods

        return (
            <Box>
                <Typography variant="h3">
                    Периоды
                </Typography>

                <ul>
                    { planningPeriods
                        .slice()
                        .sort(function(a, b) {
                            if (a.start < b.start) {
                                return 1;
                            }
                            if (a.start === b.start) {
                                return 0;
                            }
                            if (a.start > b.start) {
                                return -1;
                            }
                        })
                        .map(planningPeriod => (
                            <li key={ planningPeriod.id }>
                                <RouterLink to={ `/planningPeriods/${planningPeriod.id}` }>
                                { planningPeriod.name }
                                </RouterLink>
                                &nbsp;
                                ({ planningPeriod.start } - { planningPeriod.end })
                            </li>
                        )
                    )}
                </ul>
            </Box>
        );
    }
}

export default graphql(fetchPlanningPeriods)(PlanningPeriodsList);