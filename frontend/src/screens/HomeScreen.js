import React from 'react';
import { View, Button } from 'react-native';

export default function HomeScreen({ navigation }) {
    return (
        <View style={{flex:1,justifyContent:'center',padding:20}}>
            <Button title="Chat" onPress={() => navigation.navigate('Chat')} />
            <Button title="Meal Planner" onPress={() => navigation.navigate('MealPlanner')} />
            <Button title="Suggestions" onPress={() => navigation.navigate('Suggestions')} />
            <Button title="History" onPress={() => navigation.navigate('History')} />
            <Button title="Profile" onPress={() => navigation.navigate('Profile')} />
        </View>
    );
}
