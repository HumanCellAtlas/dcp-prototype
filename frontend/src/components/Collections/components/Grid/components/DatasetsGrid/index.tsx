import React, { FC, useState } from "react";
import { Dataset } from "src/common/entities";
import {
  CollectionHeaderCell,
  LeftAlignedHeaderCell,
  RightAlignedHeaderCell,
  StyledCollectionsGrid,
} from "src/components/Collections/components/Grid/common/style";
import { UploadedFiles } from "src/views/Collection";
import DatasetRow from "../Row/DatasetRow";
interface Props {
  datasets: Dataset[];
  uploadedFiles: UploadedFiles;
  invalidateCollectionQuery: () => void;
}

const DatasetsGrid: FC<Props> = ({
  datasets,
  uploadedFiles,
  invalidateCollectionQuery,
}) => {
  const [selected, setSelected] = useState(new Set());

  const handleSelect = (id: string) => {
    const newSelected = new Set(selected);
    if (newSelected.has(id)) newSelected.delete(id);
    else newSelected.add(id);
    setSelected(newSelected);
  };

  return (
    <StyledCollectionsGrid bordered>
      <thead>
        <tr>
          <CollectionHeaderCell>Dataset</CollectionHeaderCell>
          <LeftAlignedHeaderCell>Tissue</LeftAlignedHeaderCell>
          <LeftAlignedHeaderCell>Assay</LeftAlignedHeaderCell>
          <LeftAlignedHeaderCell>Disease</LeftAlignedHeaderCell>
          <LeftAlignedHeaderCell>Organism</LeftAlignedHeaderCell>
          <RightAlignedHeaderCell>Cell Count</RightAlignedHeaderCell>
        </tr>
      </thead>
      <tbody>
        {sortByCreatedAtAscending(datasets).map((dataset) => (
          <DatasetRow
            key={dataset.id}
            dataset={dataset}
            checkHandler={handleSelect}
            file={uploadedFiles[dataset.id]}
            invalidateCollectionQuery={invalidateCollectionQuery}
          />
        ))}
      </tbody>
    </StyledCollectionsGrid>
  );
};

function sortByCreatedAtAscending(datasets: Dataset[]): Dataset[] {
  return datasets?.sort((a, b) => a.created_at - b.created_at) || [];
}

export default DatasetsGrid;
