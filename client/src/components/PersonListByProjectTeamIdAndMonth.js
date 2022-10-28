import React, {Component} from "react";
import {gql} from '@apollo/client';
import {graphql} from '@apollo/client/react/hoc';
import Typography from '@material-ui/core/Typography';
import {Box, Link} from "@material-ui/core";
import {DataGridPro, GridToolbarContainer, GridToolbarExport} from "@mui/x-data-grid-pro";
import {Link as RouterLink} from "react-router-dom";

const fetchPersonListByProjectTeamIdAndMonth = gql`
    query PersonsByProjectTeamIdAndMonth($projectTeamId: Int, $month: Date) {
        personsByProjectTeamIdAndMonth(projectTeamId: $projectTeamId, month: $month) {
            analysisTimeSpentMonthFte
            developmentTimeSpentMonthFte
            testingTimeSpentMonthFte
            managementTimeSpentMonthFte
            incidentFixingTimeSpentMonthFte
            timeSpentMonthFte
            person {
                id
                key
                name
            }
        }
    }
`;

class PersonListByProjectTeamIdAndMonth extends Component {
    render() {
        if (this.props.data.loading) { return <div>Loading ...</div> }

        const month = this.props.match.params.month
        const personsByProjectTeamIdAndMonth = this.props.data.personsByProjectTeamIdAndMonth

        const personsTableContents = personsByProjectTeamIdAndMonth.slice()
            .sort((a, b) =>  (
                (a.person.name > b.person.name) ? 1 : (
                    (a.person.name == b.person.name) ? 0 : -1
                )
            ))
            .map(person => (
                    {
                        id: person.person.id,
                        personKey: person.person.key,
                        personName: person.person.name,
                        analysisTimeSpentMonthFte: person.analysisTimeSpentMonthFte,
                        developmentTimeSpentMonthFte: person.developmentTimeSpentMonthFte,
                        testingTimeSpentMonthFte: person.testingTimeSpentMonthFte,
                        managementTimeSpentMonthFte: person.managementTimeSpentMonthFte,
                        incidentFixingTimeSpentMonthFte: person.incidentFixingTimeSpentMonthFte,
                        timeSpentMonthFte: person.timeSpentMonthFte,
                    }
            ))
         const personsTableColumns = [
             {
                field: 'personName',
                headerName: 'ФИО',
                flex: 1,
                renderCell: (params) => (
                    <RouterLink to={ `/persons/${ params.getValue(params.id, 'personKey') }/month/${ month }` }>
                        { params.getValue(params.id, 'personName') }
                    </RouterLink>
                ),
            },
            {
                field: 'timeSpentMonthFte',
                headerName: 'Трудозатраты (FTE)',
                width: 200,
                align: 'right',
                valueFormatter: ({ value }) => value.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 }),
            },
            {
                field: 'analysisTimeSpentMonthFte',
                headerName: 'Трудозатраты аналитики (FTE)',
                width: 200,
                align: 'right',
                valueFormatter: ({ value }) => value.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 }),
            },
            {
                field: 'developmentTimeSpentMonthFte',
                headerName: 'Трудозатраты разработки (FTE)',
                width: 200,
                align: 'right',
                valueFormatter: ({ value }) => value.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 }),
            },
            {
                field: 'testingTimeSpentMonthFte',
                headerName: 'Трудозатраты тестирования (FTE)',
                width: 200,
                align: 'right',
                valueFormatter: ({ value }) => value.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 }),
            },
            {
                field: 'managementTimeSpentMonthFte',
                headerName: 'Трудозатраты управление (FTE)',
                width: 200,
                align: 'right',
                valueFormatter: ({ value }) => value.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 }),
            },
            {
                field: 'incidentFixingTimeSpentMonthFte',
                headerName: 'Трудозатраты инциденты (FTE)',
                width: 200,
                align: 'right',
                valueFormatter: ({ value }) => value.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 }),
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

export default graphql(fetchPersonListByProjectTeamIdAndMonth, {
    options: (props) => { return { variables: { projectTeamId: props.match.params.projectTeamId, month: props.match.params.month }}}
})(PersonListByProjectTeamIdAndMonth);