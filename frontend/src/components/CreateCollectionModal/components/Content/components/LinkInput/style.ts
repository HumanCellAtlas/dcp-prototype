import { Button } from "@blueprintjs/core";
import { PT_GRID_SIZE_PX } from "src/components/common/theme";
import styled from "styled-components";
import { StyledInput } from "../../style";

export const Wrapper = styled.div`
  display: flex;
`;

export const IconWrapper = styled.div`
  position: relative;
  width: ${3.5 * PT_GRID_SIZE_PX}px;
`;

export const StyledButton = styled(Button)`
  && {
    position: absolute;
    top: 20px;
    right: -${PT_GRID_SIZE_PX}px;
  }
`;

export const LinkWrapper = styled.div`
  display: flex;

  ${StyledInput}:not(:last-child) {
    margin-right: ${2 * PT_GRID_SIZE_PX}px;
  }
`;
