import { Inter } from "next/font/google";
import { RecognizeHandwrittenDigits } from "./RecognizeHandwrittenDigits";

const inter = Inter({ subsets: ["latin"] });

export default function Home() {
  return (
    <body
      className={
        inter.className + " bg-cyan-800 text-blue-100 max-w-[480px] m-auto"
      }
    >
      <header className="text-center my-4">
        <h1 className="text-xl font-bold">Self Hosted MNIST Example</h1>
        <div className="text-sm">
          This page shows an example of self hosting a TensorFlow model.
        </div>
      </header>
      <main className="m-4">
        <RecognizeHandwrittenDigits />
      </main>
    </body>
  );
}
