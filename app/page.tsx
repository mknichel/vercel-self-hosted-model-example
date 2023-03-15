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
          This page shows an example of self hosting a TensorFlow model on
          Vercel. See{" "}
          <a
            className="underline"
            href="https://github.com/mknichel/vercel-self-hosted-model-example"
          >
            GitHub
          </a>{" "}
          for more information on how it works.
        </div>
      </header>
      <main className="m-4">
        <RecognizeHandwrittenDigits />
      </main>
    </body>
  );
}
