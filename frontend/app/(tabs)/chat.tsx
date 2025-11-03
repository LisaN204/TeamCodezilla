import { View, Text, StyleSheet } from "react-native";

export default function ChatScreen() {
    return (
        <View style={styles.container}>
            <Text style={styles.title}>Chat Screen (coming soon)</Text>
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: "#FFFFFF",
        justifyContent: "center",
        alignItems: "center",
        padding: 20,
    },
    title: {
        fontSize: 22,
        fontWeight: "bold",
        color: "#000000",
        textAlign: "center",
    },
});
