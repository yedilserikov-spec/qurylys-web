export const metadata = {
  title: "Privacy Policy | Qurylys",
  description: "Privacy Policy for Qurylys",
};

export default function PrivacyPage() {
  return (
    <main className="min-h-screen bg-[#2B2B2B] text-white px-6 py-16">
      <div className="mx-auto max-w-5xl rounded-3xl border border-white/10 bg-white/5 p-10 backdrop-blur">

        <h1 className="mb-8 text-4xl font-bold text-[#2AFF00]">
          Privacy Policy
        </h1>

        <p className="mb-8 text-white/70">
          Effective date: July 14, 2026
        </p>

        <section className="space-y-6 text-white/80 leading-8">

          <div>
            <h2 className="mb-2 text-2xl font-semibold text-white">
              1. Information We Collect
            </h2>

            <ul className="list-disc ml-6 space-y-2">
              <li>Phone number</li>
              <li>User profile information</li>
              <li>Photos and uploaded files</li>
              <li>Advertisements and posts</li>
              <li>Messages between users</li>
              <li>Device information</li>
              <li>Push notification token</li>
            </ul>
          </div>

          <div>
            <h2 className="mb-2 text-2xl font-semibold text-white">
              2. How We Use Information
            </h2>

            <ul className="list-disc ml-6 space-y-2">
              <li>Provide application functionality</li>
              <li>User authentication</li>
              <li>Publish advertisements</li>
              <li>Messaging</li>
              <li>Push notifications</li>
              <li>Improve security</li>
              <li>Prevent fraud</li>
            </ul>
          </div>

          <div>
            <h2 className="mb-2 text-2xl font-semibold text-white">
              3. Data Storage
            </h2>

            <p>
              Qurylys uses Google Firebase services including Firebase
              Authentication, Cloud Firestore, Firebase Storage and Firebase
              Cloud Messaging.
            </p>
          </div>

          <div>
            <h2 className="mb-2 text-2xl font-semibold text-white">
              4. Data Sharing
            </h2>

            <p>
              We do not sell personal information. Data may only be shared when
              required by law or necessary to operate the application.
            </p>
          </div>

          <div>
            <h2 className="mb-2 text-2xl font-semibold text-white">
              5. Security
            </h2>

            <p>
              We use appropriate technical and organizational measures to
              protect user information.
            </p>
          </div>

          <div>
            <h2 className="mb-2 text-2xl font-semibold text-white">
              6. Contact
            </h2>

            <p>Email: yedilserikov@gmail.com</p>
          </div>

        </section>

      </div>
    </main>
  );
}