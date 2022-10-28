import React, {Component} from "react";
import {gql} from '@apollo/client';
import {graphql} from '@apollo/client/react/hoc';
import moment from 'moment';
import Typography from '@material-ui/core/Typography';
import {Link as RouterLink, NavLink} from "react-router-dom"
import {Box, Link} from "@material-ui/core";
import TimeSheetsByDateIssueChart from './TimeSheetsByDateIssueChart'
import {DataGridPro, GridToolbarContainer, GridToolbarExport} from "@mui/x-data-grid-pro";

const fetchPlanningPeriodPersonList = gql`
    query PlanningPeriodByIdQuery($id: Int!) {
        planningPeriodById(id: $id) {
            persons {
              personId
              personKey
              personName
              effortPerFunctionPoint
              newFunctionsTimeSpent
            }
        }
    }
`;

class PlanningPeriodPersonsList extends Component {
    render() {
        if (this.props.data.loading) { return <div>Loading ...</div> }

        const planningPeriodId = this.props.match.params.planningPeriodId

        const persons = this.props.data.planningPeriodById.persons

        const personsTableContents = persons.slice()
            .sort((a, b) =>  (
                (a.personName > b.personName) ? 1 : (
                    (a.personName == b.personName) ? 0 : -1
                )
            ))
            .map(person => (
                    {
                        id: person.personId,
                        personId: person.personId,
                        key: person.personKey,
                        name: person.personName,
                        effortPerFunctionPoint: person.effortPerFunctionPoint,
                    }
            ))

            const personsTableColumns = [
            {
                field: 'name',
                headerName: 'ФИО',
                flex: 1,
                renderCell: (params) => (
                    <RouterLink to={ `/planningPeriods/${ planningPeriodId }/persons/${ params.getValue(params.id, 'key') }` }>
                        { params.getValue(params.id, 'name') }
                    </RouterLink>
                ),
            },
            {
                field: 'effortPerFunctionPoint',
                headerName: 'Затраты на ф.т.',
                width: 200,
                align: 'right',
                valueFormatter: ({ value }) => value.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 }) ,
            },
        ];

        return (
            <Box>
                <Typography variant="h6" noWrap>
                    Команда
                </Typography>
                <div>
                    <DataGridPro
                        rows={ personsTableContents }
                        columns={ personsTableColumns }
                        autoHeight
                    />
                </div>
            </Box>
        );
    }
}

export default graphql(fetchPlanningPeriodPersonList, {
    options: (props) => { return { variables: { id: props.match.params.planningPeriodId }}}
})(PlanningPeriodPersonsList);