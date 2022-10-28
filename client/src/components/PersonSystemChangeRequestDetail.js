import React, {Component} from "react";
import {gql} from '@apollo/client';
import { graphql } from '@apollo/client/react/hoc';
import Typography from '@material-ui/core/Typography';
import {Box, Link} from "@material-ui/core";
import TimeSheetsByDateIssueChart from './TimeSheetsByDateIssueChart'
import {Link as RouterLink} from "react-router-dom";
import {DataGridPro} from "@mui/x-data-grid-pro";

const fetchPersonSystemChangeRequestTimeSheetsByDateByPersonKeyAndSystemChangeRequestKey = gql`
    query PersonSystemChangeRequestTimeSheetsByDateByPersonKeyAndSystemChangeRequestKey($personKey: String!, $systemChangeRequestKey: String!) {
        personSystemChangeRequestTimeSheetsByDateByPersonKeyAndSystemChangeRequestKey(personKey: $personKey, systemChangeRequestKey: $systemChangeRequestKey) {
            id
            date
            timeSpent
        }
    }
`;

class PersonSystemChangeRequestDetail extends Component {
    render() {
        if (this.props.data.loading) { return <div>Loading ...</div> }

        const timeSheetsByDate = this.props.data.personSystemChangeRequestTimeSheetsByDateByPersonKeyAndSystemChangeRequestKey

        const timeSheetsTableContents = timeSheetsByDate.slice()
            .sort((a, b) => ((a.date > b.date) ? 1 : ((a.date < b.date) ? -1 : 0)))
            .map(timeSheetRecord => (
                    {
                        id: timeSheetRecord.id,
                        date: timeSheetRecord.date,
                        timeSpent: timeSheetRecord.timeSpent,
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
                field: 'timeSpent',
                headerName: 'Списано (ч)',
                width: 200,
                align: 'right',
                valueFormatter: ({ value }) => value.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 }),
            },
        ];

        return (
            <Box>
                <Typography variant="h6" noWrap>
                    Тайм-шиты
                </Typography>

                <div>
                    <DataGridPro
                        rows={ timeSheetsTableContents }
                        columns={ timeSheetsTableColumns }
                        autoHeight
                    />
                </div>
            </Box>
        );
    }
}

export default graphql(fetchPersonSystemChangeRequestTimeSheetsByDateByPersonKeyAndSystemChangeRequestKey, {
    options: (props) => { return { variables: { systemChangeRequestKey: props.match.params.systemChangeRequestKey, personKey: props.match.params.personKey }}}
})(PersonSystemChangeRequestDetail);