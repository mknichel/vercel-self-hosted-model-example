"use client";

import {
  forwardRef,
  PointerEvent,
  useEffect,
  useImperativeHandle,
  useRef,
} from "react";

export interface DrawingCanvasHandle {
  clear: () => void;
  getImage: () => string;
}

export const DrawingCanvas = forwardRef((_, ref) => {
  const isDrawingRef = useRef<boolean>(false);
  const canvasRef = useRef<HTMLCanvasElement>();

  const draw = (e: PointerEvent<HTMLCanvasElement>) => {
    if (!isDrawingRef.current) {
      return;
    }
    const canvas = e.target as HTMLCanvasElement;
    const bx = canvas.getBoundingClientRect();

    // This adjustment takes into account that the canvas may have a different
    // internal width and height than the size on the screen.
    const xAdjustment = canvas.width / bx.width;
    const yAdjustment = canvas.height / bx.height;
    const pos = {
      x: (e.clientX - bx.left) * xAdjustment,
      y: (e.clientY - bx.top) * yAdjustment,
    };

    const ctx = canvas.getContext("2d");
    if (!ctx) {
      return;
    }
    ctx.beginPath();
    ctx.arc(pos.x, pos.y, 3, 0, 2 * Math.PI);
    ctx.fillStyle = "black";
    ctx.fill();
  };
  const handleStartDraw = (e: PointerEvent<HTMLCanvasElement>) => {
    isDrawingRef.current = true;
    draw(e);
  };
  const handleEndDraw = (e: PointerEvent<HTMLCanvasElement>) => {
    isDrawingRef.current = false;
  };
  const handlePointerMove = (e: PointerEvent<HTMLCanvasElement>) => {
    draw(e);
  };

  useImperativeHandle(ref, () => ({
    clear() {
      const canvas = canvasRef.current;
      const ctx = canvas?.getContext("2d");
      if (!canvas || !ctx) {
        return;
      }
      ctx.fillStyle = "white";
      ctx.fillRect(0, 0, canvas.width, canvas.height);
    },
    getImage() {
      const canvas = canvasRef.current;
      return canvas?.toDataURL();
    },
  }));

  useEffect(() => {
    // Make the canvas square since the server wants square images.
    if (canvasRef.current) {
      const canvas = canvasRef.current;
      canvas.width = canvas.height;
    }
  }, []);

  return (
    <div className="w-full">
      <canvas
        className="w-full border-black border-2 rounded-lg bg-white"
        style={{ touchAction: "none" }}
        ref={canvasRef}
        onPointerDown={handleStartDraw}
        onPointerUp={handleEndDraw}
        onPointerMove={handlePointerMove}
      ></canvas>
    </div>
  );
});
