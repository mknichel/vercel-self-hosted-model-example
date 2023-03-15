import "./globals.css";

export const metadata = {
  title: "Vercel Self Hosted TensorFlow Example",
  description:
    "An example of self hosting a TensorFlow model on Vercel using the Python runtime.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
