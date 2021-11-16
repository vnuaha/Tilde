import React from "react";
import GitHubIcon from "@mui/icons-material/GitHub";
import Typography from "@mui/material/Typography";
import { makeStyles } from "@mui/material/styles";

import Table from "@mui/material/Table";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableBody";
import TableBody from "@mui/material/TableBody";
import TableRow from "@mui/material/TableRow";
import TableCell from "@mui/material/TableCell";
import Tabs from "@mui/material/Tabs";
import Tab from "@mui/material/Tab";
import Box from "@mui/material/Box";

const useStyles = makeStyles((theme) => ({
  container: {
    maxHeight: 240,
  },

  tabPanel: {
    minWidth: theme.spacing(200),
  },
}));

function TabPanel(props) {
  const { children, value, index, ...other } = props;
  const classes = useStyles();
  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`wrapped-tabpanel-${index}`}
      aria-labelledby={`wrapped-tab-${index}`}
      className={classes.tabPanel}
      {...other}
    >
      {value === index && <Box p={3}>{children}</Box>}
    </div>
  );
}

// const CommitsTable = ({ commits }) => {
//   const classes = useStyles();
//   return (
//     <TableContainer className={classes.container}>
//       <Table stickyHeader aria-label="sticky table">
//         <TableHead>
//           <TableRow>
//             <TableCell>Datetime</TableCell>
//             <TableCell>Branch</TableCell>
//             <TableCell>Author Email</TableCell>
//             <TableCell>Author Github</TableCell>
//             <TableCell>Message</TableCell>
//             <TableCell>Hash</TableCell>
//           </TableRow>
//         </TableHead>
//         <TableBody>
//           {commits.map((commit) => {
//             return (
//               <TableRow key={commit.id}>
//                 <TableCell>{commit.datetime}</TableCell>
//                 <TableCell>{commit.branch}</TableCell>
//                 <TableCell>{commit.authorEmail}</TableCell>
//                 <TableCell>{commit.authorGithubName}</TableCell>
//                 <TableCell>{commit.message}</TableCell>
//                 <TableCell>{commit.commitHash}</TableCell>
//               </TableRow>
//             );
//           })}
//         </TableBody>
//       </Table>
//     </TableContainer>
//   );
// };

const PullRequestsTable = ({ pullRequests, repository }) => {
  const classes = useStyles();
  return (
    <TableContainer className={classes.container}>
      <Table stickyHeader aria-label="sticky table">
        <TableHead>
          <TableRow>
            <TableCell>Title</TableCell>
            <TableCell>State</TableCell>
            <TableCell>Body</TableCell>
            <TableCell>Updated at</TableCell>
            <TableCell>Closed at</TableCell>
            <TableCell>Merged at</TableCell>
            <TableCell>Created at</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {pullRequests.map((pr) => {
            return (
              <TableRow key={pr.id}>
                <TableCell>
                  <a
                    href={`https://github.com/${repository.fullName}/pull/${pr.number}`}
                  >
                    {pr.title}
                  </a>
                </TableCell>
                <TableCell>{pr.state}</TableCell>
                {/* <TableCell>{pr.authorGithubName}</TableCell>
                <TableCell>{pr.assignees}</TableCell> */}
                <TableCell>{pr.body}</TableCell>
                <TableCell>{pr.updatedAt}</TableCell>
                <TableCell>{pr.closedAt}</TableCell>
                <TableCell>{pr.mergedAt}</TableCell>
                <TableCell>{pr.createdAt}</TableCell>
              </TableRow>
            );
          })}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default ({
  repository,
  // currentCommits,
  currentPullRequests,
  tabValue,
  handleChangeTab,
}) => {
  return (
    <React.Fragment>
      <Typography variant="h6">Repo Details</Typography>
      {repository ? (
        <React.Fragment>
          <Tabs
            value={tabValue}
            indicatorColor="primary"
            textColor="primary"
            onChange={handleChangeTab}
            aria-label="disabled tabs example"
          >
            <Tab label="Details" />
            {/* <Tab label="Commits" /> */}
            <Tab label="Pull Requests" />
          </Tabs>
          <TabPanel value={tabValue} index={0}>
            <Typography>
              <GitHubIcon />{" "}
              <a
                href={`https://github.com/${repository.fullName}`}
                target="_blank"
                rel="noopener noreferrer"
              >
                {" "}
                {repository.fullName}
              </a>
            </Typography>

            <Typography variant="subtitle2">Created At</Typography>
            <Typography>{repository.createdAt}</Typography>
            <Typography variant="subtitle2">Clone url</Typography>
            <Typography>{repository.sshUrl}</Typography>
          </TabPanel>

          {/* <TabPanel value={tabValue} index={1}>
            <CommitsTable commits={currentCommits} />
          </TabPanel> */}
          <TabPanel value={tabValue} index={1}>
            <PullRequestsTable
              pullRequests={currentPullRequests}
              repository={repository}
            />
          </TabPanel>
        </React.Fragment>
      ) : (
        <Typography>Loading...</Typography>
      )}
    </React.Fragment>
  );
};
