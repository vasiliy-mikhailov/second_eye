import React, {Component} from "react";
import {gql} from '@apollo/client';
import { graphql } from '@apollo/client/react/hoc';
import Typography from '@material-ui/core/Typography';
import {Box, Link} from "@material-ui/core";
import TimeSheetsByDateIssueChart from "./TimeSheetsByDateIssueChart";
import {Link as RouterLink} from "react-router-dom";
import {DataGridPro} from "@mui/x-data-grid-pro";
import ReengineeringByDatePeriodChart from "./ReengineeringByDatePeriodChart";

const fetchSystemById = gql`
    query SystemById($id: Int!) {
        systemById(id: $id) {
            id
            estimate
            timeLeft
            name
            newFunctionsFullTimeEquivalentPrevious28Days
            newFunctionsTimeSpentPrevious28Days
            
            persons {
                id
                
                person {
                    id
                    key
                    name
                    isActive
                    newFunctionsFullTimeEquivalentPrevious28Days
                }
                
                newFunctionsTimeSpent
                
                newFunctionsFullTimeEquivalentPrevious28Days
            }
        }
    }
`;

class SystemDetail extends Component {
    render() {
        if (this.props.data.loading) { return <div>Loading ...</div> }
        const systemId = this.props.match.params.systemId
        const system = this.props.data.systemById

        const systemName = system.name
        const estimate = system.estimate

        const persons = system.persons

        const personsTableContents = persons.slice()
            .sort((a, b) =>  (
                (a.newFunctionsFullTimeEquivalentPrevious28Days > b.newFunctionsFullTimeEquivalentPrevious28Days) ? -1 : (
                    (a.newFunctionsFullTimeEquivalentPrevious28Days == b.newFunctionsFullTimeEquivalentPrevious28Days) ? 0 : 1
                )
            ))
            .map(person => (
                    {
                        id: person.id,
                        personId: person.person.id,
                        key: person.person.key,
                        name: person.person.name,
                        newFunctionsTimeSpent: person.newFunctionsTimeSpent,
                        newFunctionsFullTimeEquivalentPrevious28DaysTotal: person.person.newFunctionsFullTimeEquivalentPrevious28Days,
                        newFunctionsFullTimeEquivalentPrevious28Days: person.newFunctionsFullTimeEquivalentPrevious28Days,
                        isActive: person.person.isActive,
                    }
            ))

        const personsTableColumns = [
            {
                field: 'name',
                headerName: 'ФИО',
                flex: 1,
                renderCell: (params) => (
                    <RouterLink to={ `/persons/${ params.getValue(params.id, 'key') }` }>
                        { params.getValue(params.id, 'name') }
                    </RouterLink>
                ),
            },
            {
                field: 'isActive',
                headerName: 'Активный',
                flex: 1,
                renderCell: (params) => (
                    params.getValue(params.id, 'isActive') ? "Да" : "Нет"
                ),
            },
            {
                field: 'newFunctionsTimeSpent',
                headerName: 'Новый функционал: списано всего (ч)',
                width: 200,
                align: 'right',
                valueFormatter: ({ value }) => value.toLocaleString(undefined, { maximumFractionDigits: 0 }),
            },
            {
                field: 'newFunctionsFullTimeEquivalentPrevious28Days',
                headerName: 'Новый функционал: фактический FTE за 28 дней на эту систему',
                width: 200,
                align: 'right',
                valueFormatter: ({ value }) => (value).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2}),
            },
            {
                field: 'newFunctionsFullTimeEquivalentPrevious28DaysTotal',
                headerName: 'Новый функционал: фактический FTE за 28 дней на все системы',
                width: 200,
                align: 'right',
                valueFormatter: ({ value }) => (value).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2}),
            },
        ];

        return (
            <Box>
                <Typography variant="body" noWrap>
                    Система { systemName } &nbsp;
                    <br />
                    <br />
                </Typography>

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

export default graphql(fetchSystemById, {
    options: (props) => { return { variables: { id: props.match.params.systemId }}}
})(SystemDetail);