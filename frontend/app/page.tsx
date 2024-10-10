"use client";
import React, { useEffect, useState } from "react";
import { PlaceholdersAndVanishInput } from "@/components/ui/placeholders-and-vanish-input";
import { Button, Chip, CircularProgress } from "@nextui-org/react";
import { User, Link } from "@nextui-org/react";

export default function Home() {
  const placeholders = [
    "Enter your joke here!",
    "Yo mama is so fat ...",
    "There was a pregnant ant ...",
    "An asian guy entered the bar ...",
    "I made a chemistry joke ...",
  ];
  const [joke, setJoke] = useState<string>("");
  const [currentJoke, setCurrentJoke] = useState<string>("");
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setJoke(e.target.value);
  };
  const onSubmit = () => {
    if(joke.length==0) return;
    setIsLoading(true);
    setResults(false);
    setTimeout(() => {
      console.log("fired");
      setIsLoading(false); 
      setResults(true);
      setCurrentJoke(joke);
      setJoke("");
    }, 2000);
  };
  type ButtonType = "warning" | "default" | "primary" | "secondary" | "success" | "danger" | undefined;
  const [results, setResults] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [humorScore, setHumorScore] = useState(87);
  const [humorColor, setHumorColor] = useState<ButtonType>("warning")
  const [humorText, setHumorText] = useState("Good")
  const [offenseScore, setOffenseScore] = useState(95);
  const [offenseColor, setOffenseColor] = useState<ButtonType>("warning")
  const [offenseText, setOffenseText] = useState("Offensive")

  useEffect(() => {
    if(humorScore <=25 ){
      setHumorColor("danger")
      setHumorText("Mehh!")
    }else if(humorScore > 25 && humorScore <= 50){
      setHumorColor("warning")
      setHumorText("Midd!")
    }else if(humorScore > 50 && humorScore <= 75){
      setHumorColor("primary")
      setHumorText("Hmm! Good")
    }else if(humorScore > 75 && humorScore <= 100){
      setHumorColor("success")
      setHumorText("Damn Nice!")
    }
  }, [humorScore])

  useEffect(() => {
    if(offenseScore <=25 ){
      setOffenseColor("success")
      setOffenseText("Safe!")
    }else if(offenseScore > 25 && offenseScore <= 50){
      setOffenseColor("default")
      setOffenseText("Almost safe!")
    }else if(offenseScore > 50 && offenseScore <= 75){
      setOffenseColor("warning")
      setOffenseText("Twitter Cancel")
    }else if(offenseScore > 75 && offenseScore <= 100){
      setOffenseColor("danger")
      setOffenseText("Jail !")
    }
  }, [offenseScore])

  return (
    <div className="flex h-screen w-screen flex-col items-center gap-10 bg-[#1E1E1E] px-5 py-10">
      <div className="flex w-[97vw] flex-row justify-center">
        <div className="flex w-[50vw] flex-row items-center">
          <div className="flex-grow">
            <PlaceholdersAndVanishInput
              placeholders={placeholders}
              onChange={handleChange}
              onSubmit={onSubmit}
            />
          </div>
        </div>
      </div>
      {isLoading && (
        <div className="h-[50vh] w-[60vw] flex flex-col justify-center items-center">
          <CircularProgress color="warning" aria-label="Loading..."/>
        </div>
      )}
      {results && (
        <div className="flex flex-col items-center gap-10">
        <div className="flex flex-row gap-10">
          <div className="shadow-custom h-fit w-[20vw] rounded-lg p-5">
            <div>
              <p className="text-medium text-gray-400">Humor Score:</p>
              <p className={`text-2xl text-`+humorColor}>{humorScore}</p>
            </div>
            <Button color={humorColor} className="mt-5">
              {humorText}
            </Button>
          </div>
          <div className="shadow-custom h-fit w-[20vw] rounded-lg p-5">
            <div>
              <p className="text-medium text-gray-400">Offense Score:</p>
              <p className={`text-2xl text-`+offenseColor}>{offenseScore}</p>
            </div>
            <Button color={offenseColor} className="mt-5">
              {offenseText}
            </Button>
          </div>
        </div>
        <div className="w-[60vw] flex flex-col items-center max-h-[38vh] overflow-y-scroll">
          <p className="text-gray-400 text-medium mt-5">{`"${currentJoke}"`}</p>
          <p className="text-gray-500 text-[0.65rem]">-you</p>
        </div>
        </div>
      )}
      <div className="fixed bottom-4 flex w-[97vw] justify-between gap-2">
        <div className="flex gap-2">
          <Chip
            color="warning"
            variant="dot"
            onClick={() => window.open("https://github.com/avneets2103/", "_blank", "noopener,noreferrer")}
            className="select-none text-gray-400"
          >
            Source Code
          </Chip>
          <Chip
            color="warning"
            variant="dot"
            onClick={() => window.location.href = "/about"}
            className="select-none text-gray-400"
          >
            About Us
          </Chip>
        </div>
        <div>
          <User
            name="Avneet Singh"
            description={
              <Link
                href="https://www.linkedin.com/in/avneets2103"
                size="sm"
                isExternal
                className="text-yellow-600"
              >
                @avneets2103
              </Link>
            }
            className="text-gray-300"
            avatarProps={{
              src: "/Icons/me.jpeg",
            }}
          />
        </div>
      </div>
    </div>
  );
}
