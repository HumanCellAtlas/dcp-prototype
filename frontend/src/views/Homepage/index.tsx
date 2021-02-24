import Head from "next/head";
import React, { FC } from "react";
import Collections from "src/components/Collections";

const Homepage: FC = () => {
  const handleCSV = async (event) => {
    const timeStart = Date.now();

    const file = event.target.files[0];
    const fileReader = new FileReader();
    fileReader.readAsText(file);

    const csv = await file.text();

    const rows = csv.split(/\r\n|\n/);
    const headers = rows[0].split(/,(?![^"]*"(?:(?:[^"]*"){2})*[^"]*$)/);

    const result = rows.map((row) => row.split(","));
    const json = JSON.stringify({ result });

    // DEBUG
    // DEBUG
    // DEBUG
    console.log("--------file", file);
    console.log("--------headers", headers);
    console.log("--------result", result);
    console.log("--------json", json);

    window.alert(`DONE! It took ${Date.now() - timeStart} ms`);
  };

  return (
    <>
      <Head>
        <title>cellxgene | Homepage</title>
      </Head>
      <input type="file" accept="csv" onChange={handleCSV} />
      <Collections />
    </>
  );
};

export default Homepage;
