import Head from "next/head";
import React, { FC } from "react";
import Collections from "src/components/Collections";

const Homepage: FC = () => {
  return (
    <>
      <Head>
        <title>cellxgene | Homepage</title>
      </Head>
      <Collections />
    </>
  );
};

export default Homepage;
