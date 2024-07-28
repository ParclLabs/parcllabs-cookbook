declare module "react-plotly.js" {
  import * as Plotly from "plotly.js-dist";
  import * as React from "react";

  interface PlotProps {
    data: Plotly.PlotData[];
    layout?: Partial<Plotly.Layout>;
    config?: Partial<Plotly.Config>;
    useResizeHandler?: boolean;
    style?: React.CSSProperties;
  }

  const Plot: React.FC<PlotProps>;
  export default Plot;
}
