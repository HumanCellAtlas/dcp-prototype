import React, { FC } from "react";
import { ACCESS_TYPE } from "src/common/entities";
import { CollectionResponse } from "src/common/queries/collections";
import CollectionRow from "./CollectionRow";
import {
  CollectionHeaderCell,
  LeftAlignedHeaderCell,
  RightAlignedHeaderCell,
  StyledCollectionsGrid,
} from "./style";

interface Props {
  collections: CollectionResponse[];
  accessType: ACCESS_TYPE;
}

const CollectionsGrid: FC<Props> = ({ collections, accessType }) => {
  return (
    <StyledCollectionsGrid bordered>
      <thead>
        <tr>
          <CollectionHeaderCell>Collection</CollectionHeaderCell>
          <LeftAlignedHeaderCell>Tissue</LeftAlignedHeaderCell>
          <LeftAlignedHeaderCell>Assay</LeftAlignedHeaderCell>
          <LeftAlignedHeaderCell>Disease</LeftAlignedHeaderCell>
          <LeftAlignedHeaderCell>Organism</LeftAlignedHeaderCell>
          <RightAlignedHeaderCell>Cell Count</RightAlignedHeaderCell>
        </tr>
      </thead>
      <tbody>
        {collections?.map((collection) => (
          <CollectionRow
            id={collection.id}
            key={collection.id}
            visibility={collection.visibility}
            {...{ accessType }}
          />
        ))}
      </tbody>
    </StyledCollectionsGrid>
  );
};

export default CollectionsGrid;
