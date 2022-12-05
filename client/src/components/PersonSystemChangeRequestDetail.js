import React from "react";
import {gql, useQuery} from '@apollo/client';
import Typography from '@material-ui/core/Typography';
import {Box} from "@material-ui/core";
import {DataGridPro} from "@mui/x-data-grid-pro";
import {useParams} from "react-router-dom";

const fetchPersonSystemChangeRequestTimeSheetsByDateByPersonKeyAndSystemChangeRequestKey = gql`
    query PersonSystemChangeRequestTimeSheetsByDateByPersonKeyAndSystemChangeRequestKey($personKey: String!, $systemChangeRequestKey: String!) {
        personSystemChangeRequestTimeSheetsByDateByPersonKeyAndSystemChangeRequestKey(personKey: $personKey, systemChangeRequestKey: $systemChangeRequestKey) {
            id
            date
            functionPointsEffort
        }
    }
`;

function PersonSystemChangeRequestDetail() {
    const {systemChangeRequestKey, personKey} = useParams();
    const {
        loading,
        error,
        data
    } = useQuery(fetchPersonSystemChangeRequestTimeSheetsByDateByPersonKeyAndSystemChangeRequestKey, {
        variables: {systemChangeRequestKey: systemChangeRequestKey, personKey: personKey}
    });

    if (loading) return 'Loading ...'

    if (error) return `Error! ${error.message}`

    const timeSheetsByDate = data.personSystemChangeRequestTimeSheetsByDateByPersonKeyAndSystemChangeRequestKey

    const timeSheetsTableContents = timeSheetsByDate.slice()
        .sort((a, b) => ((a.date > b.date) ? 1 : ((a.date < b.date) ? -1 : 0)))
        .map(timeSheetRecord => (
            {
                id: timeSheetRecord.id,
                date: timeSheetRecord.date,
                functionPointsEffort: timeSheetRecord.functionPointsEffort,
            }
        ))

    const timeSheetsTableColumns = [
        {
            field: 'date',
            headerName: 'Дата',
            width: 200,
            align: 'center',
        },
        {
            field: 'functionPointsEffort',
            headerName: 'Списано аналитика, разработка, менеджмент (ч)',
            width: 200,
            align: 'right',
            valueFormatter: ({value}) => value.toLocaleString(undefined, {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            }),
        },
    ];

    return (
        <Box>
            <Typography variant="h6" noWrap>
                Тайм-шиты
            </Typography>

            <div>
                <DataGridPro
                    rows={timeSheetsTableContents}
                    columns={timeSheetsTableColumns}
                    autoHeight
                />
            </div>
        </Box>
    );
}

export default PersonSystemChangeRequestDetail;