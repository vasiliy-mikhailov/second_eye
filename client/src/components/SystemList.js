import React, {Component} from "react";
import {gql} from '@apollo/client';
import { graphql } from '@apollo/client/react/hoc';
import Typography from '@material-ui/core/Typography';
import {Box, Link} from "@material-ui/core";
import {Link as RouterLink} from "react-router-dom";
import { DataGridPro,} from '@mui/x-data-grid-pro';

const fetchSystems = gql`
    query Systems {
        systems {
            id
            estimate
            timeLeft
            name
            newFunctionsFullTimeEquivalentPrevious28Days
            newFunctionsTimeSpentPrevious28Days
        }
    }
`;

class SystemList extends Component {
    render() {
        if (this.props.data.loading) { return <div>Loading ...</div> }

        const systems = this.props.data.systems

        const systemsTableContents = systems.slice()
            .sort((a, b) => ((a.name > b.name) ? 1 : ((a.name < b.name) ? -1 : 0)))
            .filter(system => (
                   system.newFunctionsFullTimeEquivalentPrevious28Days > 0
                )
            )
            .map(system => (
                    {
                        id: system.id,
                        name: system.name,
                        newFunctionsFullTimeEquivalentPrevious28Days: system.newFunctionsFullTimeEquivalentPrevious28Days,
                    }
            ))

        const systemsTableColumns = [
            {
                field: 'name',
                headerName: 'Название',
                flex: 1,
                renderCell: (params) => (
                    <RouterLink to={ `/systems/${ params.getValue(params.id, 'id') }` }>
                        { params.getValue(params.id, 'name') }
                    </RouterLink>
                ),
            },
            {
                field: 'newFunctionsFullTimeEquivalentPrevious28Days',
                headerName: 'Новый функционал: фактический FTE за 28 дней',
                width: 200,
                align: 'right',
                valueFormatter: ({ value }) => (value).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2}),
            },
        ];

        return (
            <Box>
                <Typography variant="h6" noWrap>
                    Системы
                </Typography>

                <div>
                    <DataGridPro
                        rows={ systemsTableContents }
                        columns={ systemsTableColumns }
                        autoHeight
                    />
                </div>
            </Box>
        );
    }
}

export default graphql(fetchSystems)(SystemList);