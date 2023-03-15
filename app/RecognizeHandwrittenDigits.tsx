"use client";

import { useCallback, useRef, useState } from "react";
import { DrawingCanvas, DrawingCanvasHandle } from "./DrawingCanvas";

export function RecognizeHandwrittenDigits() {
  const canvasRef = useRef<DrawingCanvasHandle>();
  const [recognizedDigit, setRecognizedDigit] = useState<number>();

  const recognizeDigit = async () => {
    const options = {
      method: "POST",
      body: canvasRef.current?.getImage(),
    };
    const resp = await fetch("/api/recognize-digit", options);
    const predictions = (await resp.json()) as number[];
    const maxPrediction = Math.max(...predictions);
    if (maxPrediction < 0.3) {
      setRecognizedDigit(undefined);
    } else {
      setRecognizedDigit(predictions.indexOf(maxPrediction));
    }
  };

  return (
    <div className="max-w-[240px] m-auto">
      <DrawingCanvas ref={canvasRef} />
      <div className="text-center my-2">
        {typeof recognizedDigit === "number" ? (
          <span>Recognized digit: {recognizedDigit}</span>
        ) : (
          <span>No digit recognized</span>
        )}
      </div>
      <div className="text-center flex gap-2 justify-center mt-2">
        <button
          className="rounded-lg border-white border-2 p-2"
          onClick={recognizeDigit}
        >
          Recognize
        </button>
        <button
          className="rounded-lg border-white border-2 p-2"
          onClick={() => canvasRef.current?.clear()}
        >
          Clear
        </button>
      </div>
    </div>
  );
}
