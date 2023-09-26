import logo from "./logo.svg";
import "./App.css";
import {
  Box,
  Button,
  Card,
  CardBody,
  CardHeader,
  Divider,
  Heading,
  Spinner,
  Stack,
  StackDivider,
  Textarea,
  Text,
} from "@chakra-ui/react";
import { useEffect, useState } from "react";
import axios from "axios";

const baseUrl = "http://localhost:8005";

function App() {
  const [loggingIn, setLoggingIn] = useState(false);
  const [loggedIn, setLoggedIn] = useState(false);
  const [userName, setUserName] = useState("");
  const [policy, setPolicy] = useState("");
  const [policyResults, setPolicyResults] = useState({});
  const [checkingPolicy, setCheckingPolicy] = useState(false);
  useEffect(() => {
    if (!loggedIn) {
      retrieveLogin();
    }
  }, [loggedIn]);
  const login = async () => {
    setLoggingIn(true);
    try {
      const { data, status } = await axios.get(`${baseUrl}/login`, {
        withCredentials: true,
        headers: {
          Accept: "application/json",
        },
      });
      window.location.href = data.auth_url;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        console.log("error message: ", error.message);
        return {};
      } else {
        console.log("unexpected error: ", error);
        return {};
      }
    }
  };
  const retrieveLogin = async () => {
    try {
      setLoggingIn(true);
      const { data, status } = await axios.get(`${baseUrl}/user_info`, {
        withCredentials: true,
        headers: {
          Accept: "application/json",
        },
      });
      if (data.loggedIn) {
        setUserName(data.name);
        setLoggedIn(true);
      }
      setLoggingIn(false);
    } catch (error) {
      setLoggingIn(false);
      if (axios.isAxiosError(error)) {
        console.log("error message: ", error.message);
        return {};
      } else {
        console.log("unexpected error: ", error);
        return {};
      }
    }
  };
  const logout = async () => {
    try {
      setLoggingIn(true);
      const { data, status } = await axios.get(`${baseUrl}/logout`, {
        withCredentials: true,
        headers: {
          Accept: "application/json",
        },
      });
      setLoggedIn(false);
      setUserName("");
    } catch (error) {
      setLoggingIn(false);
      if (axios.isAxiosError(error)) {
        console.log("error message: ", error.message);
        return {};
      } else {
        console.log("unexpected error: ", error);
        return {};
      }
    }
  };
  const checkPolicy = async () => {
    if (policy !== "") {
      try {
        setCheckingPolicy(true);
        const { data, status } = await axios.post(
          `${baseUrl}/unstructured`,
          { policy: policy },
          {
            withCredentials: true,
            headers: {
              Accept: "application/json",
            },
          },
        );
        setPolicyResults(data);
        setCheckingPolicy(false);
      } catch (error) {
        setCheckingPolicy(false);
        if (axios.isAxiosError(error)) {
          console.log("error message: ", error.message);
          return {};
        } else {
          console.log("unexpected error: ", error);
          return {};
        }
      }
    }
  };
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo Box" alt="logo" />
        <div className="Box">
          {!loggingIn && !loggedIn && (
            <Button colorScheme="blue" onClick={login}>
              Login
            </Button>
          )}
          {loggedIn && userName && <div>Welcome {userName}!</div>}
          {loggedIn && (
            <Button colorScheme="blue" onClick={logout}>
              Logout
            </Button>
          )}
          <Divider className="Divider" />
          {loggedIn && (
            <div>
              <h5>Policy</h5>
              {!checkingPolicy && (
                <div>
                  <Textarea
                    className="Policy"
                    value={policy}
                    onChange={(event) => {
                      event.preventDefault();
                      setPolicy(event.target.value);
                    }}
                  />
                  <div className="ButtonContainer">
                    <Button
                      className="Button"
                      colorScheme="green"
                      onClick={checkPolicy}
                    >
                      Evaluate Policy
                    </Button>
                    <Button
                      className="Button"
                      colorScheme="blue"
                      onClick={() => setPolicy("")}
                    >
                      Clear Policy
                    </Button>
                  </div>
                </div>
              )}
              {checkingPolicy && <Spinner />}
              {Object.keys(policyResults).length > 0 && (
                <div className="PolicyResults">
                  <Card>
                    <CardHeader>
                      <Heading size="md">Policy Evaluation</Heading>
                    </CardHeader>
                    <CardBody>
                      <Stack divider={<StackDivider />} spacing="4">
                        <Box>
                          <Heading size="xs" textTransform="uppercase">
                            Contribution Periods
                          </Heading>
                          <Text pt="2" fontSize="sm">
                            {policyResults.periods}
                            <br />
                            {policyResults.stipulation &&
                              `* ${policyResults.stipulation}`}
                          </Text>
                        </Box>
                        <Box>
                          <Heading size="xs" textTransform="uppercase">
                            Contribution Limits
                          </Heading>
                          <Text pt="2" fontSize="sm">
                            Minimum Contribution{" "}
                            {policyResults.minimum_contribution
                              ? policyResults.minimum_contribution
                              : "$.01"}
                            &nbsp;&nbsp; Maximum Contribution{" "}
                            {policyResults.maximum_contribution}
                          </Text>
                        </Box>
                      </Stack>
                    </CardBody>
                  </Card>
                </div>
              )}
            </div>
          )}
        </div>
      </header>
    </div>
  );
}

export default App;
