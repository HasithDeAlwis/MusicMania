import React, { useEffect, useState } from "react";
import { Flex, Box, Text, Image, Link } from "@chakra-ui/react";
import spotify from "./profile/assets/spotify.svg";
import { useHistory } from "react-router-dom";
const UserColumnCard = (props) => {
  const [user, setUser] = useState();
  const history = useHistory();
  useEffect(() => {
    setUser(() => {
      return props.user;
    });
  }, []);
  const handleNewProfile = () => {
    history.push(`/profile?user=${user.token}`);
  };

  return (
    <>
      {user && (
        <Flex
          flexShrink={0}
          bgColor={"#22092C"}
          boxShadow="4px 4px 0 0 #F05941, 8px 8px 0 0  #22092C"
          transition={"200ms"}
          _hover={{
            boxShadow: "6px 6px 0 0 #F05941, 10px 10px 0 0  #22092C",
          }}
          flexDir={{ base: "column", lg: "row" }}
          padding={2}
        >
          <Box
            flexBasis={"30%"}
            cursor={"pointer"}
            alignSelf={{ base: "center", lg: "start" }}
            boxShadow="4px 4px 0 0 #F05941, 8px 8px 0 0  white"
            transition={"200ms"}
            _hover={{
              boxShadow: "6px 6px 0 0 #F05941, 10px 10px 0 0  white",
            }}
            marginBottom={2}
            marginX={2}
          >
            <Image
              src={user["profile-picture"]}
              alt={`${user.id}'s profile picture`}
            ></Image>
          </Box>
          <Box flexBasis="100%" display={"flex"} flexDir="column" padding={2}>
            <Box
              marginTop={2}
              textColor="white"
              fontFamily={"Poppins"}
              fontWeight={"500"}
              order={{ base: 2, lg: 0 }}
            >
              <Text>Compatibility Score: {user.score}</Text>
            </Box>
            <Box order={{ base: 3, lg: 1 }} fontWeight={"500"}>
              <Text textColor="white">
                Favourite Artists:{" "}
                {user["favourite-artists"].map((artist, index) =>
                  index != 0 ? ", " + artist : artist
                )}
              </Text>
              <Text textColor="white">
                Favourite Song: {user["favourite-songs"][0]} by
                {user["favourite-songs"][1].map((artist, index) =>
                  index != 0 ? ", " + artist : " " + artist
                )}
              </Text>
            </Box>
            <Box
              marginTop="auto"
              marginRight="auto"
              alignSelf={{ base: "end" }}
              _hover={{ textColor: "#AFEFEE", textDecor: "underline" }}
              textColor={"white"}
              cursor={"pointer"}
              order={{ base: 0, lg: 3 }}
              onClick={handleNewProfile}
            >
              <Text fontSize={"20px"} fontFamily={"Poppins"} fontWeight={"900"}>
                {user.username}
              </Text>
              <Text fontFamily={"Poppins"}>{user.id}</Text>
            </Box>
          </Box>
          <Link
            href={user.link}
            ml={"auto"}
            minW={{ base: "13%", md: "10%", lg: "7%" }}
            padding={1}
          >
            <Box>
              <Image
                minW={"100%"}
                objectFit="cover"
                alt="spotify logo"
                src={spotify}
              ></Image>
            </Box>
          </Link>
        </Flex>
      )}
    </>
  );
};

export default UserColumnCard;
