import SwiftUI
import DotLottie

struct HomeView: View {
    @State private var isConnected = false

    var body: some View {
        NavigationStack {
            ZStack {
                // Soft dark gray background
                Color(UIColor(red: 0.15, green: 0.15, blue: 0.16, alpha: 1.0))
                    .ignoresSafeArea()

                VStack(spacing: 40) {
                    // App logo (add "AppLogo" asset)
                    Image("AppLogo")
                        .resizable()
                        .scaledToFit()
                        .frame(width: 120, height: 120)
                        .padding(.top, 80)

                    // Use DotLottieAnimation with the local file name and config
                    DotLottieAnimation(
                        fileName: "Connection", // Looks for Connection.lottie in the app bundle
                        config: AnimationConfig(
                            autoplay: true,
                            loop: true // Set loop to true
                            speed: 0.5 // Set speed to half
                        )
                    )
                    .view() // Call .view() to get the SwiftUI View
                    .frame(width: 180, height: 180)


                    // Status text
                    Text(isConnected ? "Connected!" : "Connecting...")
                        .font(.title2)
                        .foregroundColor(isConnected ? .green : .yellow)
                        .bold()
                        .padding(.bottom, 80)
                }
            }
            .navigationBarHidden(true)
            .navigationDestination(isPresented: $isConnected) {
                MainView()
            }
        }
        .preferredColorScheme(.dark)
        .onAppear {
            // Ensure Connection.lottie is included in your app's "Copy Bundle Resources"
            DispatchQueue.main.asyncAfter(deadline: .now() + 2) {
                isConnected = true
            }
        }
    }
}
