import React from "react";
import {gql, useQuery} from '@apollo/client';
import Typography from '@material-ui/core/Typography';
import {Box} from "@material-ui/core";
import {Link as RouterLink} from "react-router-dom";
import {DataGridPro,} from '@mui/x-data-grid-pro';

const fetchSystems = gql`
    query Systems {
        systems {
            id
            estimate
            timeLeft
            name
            timeSpentChrononFte
            timeSpentChronon
        }
    }
`;

function SystemList() {
    const {loading, error, data} = useQuery(fetchSystems);

    if (loading) return 'Loading ...'

    if (error) return `Error! ${error.message}`

    const systems = data.systems

    const systemsTableContents = systems.slice()
        .sort((a, b) => ((a.name > b.name) ? 1 : ((a.name < b.name) ? -1 : 0)))
        .filter(system => (
                system.timeSpentChrononFte > 0
            )
        )
        .map(system => (
            {
                id: system.id,
                name: system.name,
                timeSpentChrononFte: system.timeSpentChrononFte,
            }
        ))

    const systemsTableColumns = [
        {
            field: 'name',
            headerName: 'Название',
            flex: 1,
            renderCell: (params) => (
                <RouterLink to={`/systems/${params.getValue(params.id, 'id')}`}>
                    {params.getValue(params.id, 'name')}
                </RouterLink>
            ),
        },
        {
            field: 'timeSpentChrononFte',
            headerName: 'Трудомощность, FTE',
            width: 200,
            align: 'right',
            valueFormatter: ({value}) => (value).toLocaleString(undefined, {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            }),
        },
    ];

    return (
        <Box>
            <Typography variant="h6" noWrap>
                Системы
            </Typography>

            <div>
                <DataGridPro
                    rows={systemsTableContents}
                    columns={systemsTableColumns}
                    autoHeight
                />
            </div>
        </Box>
    );
}

export default SystemList;