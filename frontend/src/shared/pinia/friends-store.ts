import {defineStore} from "pinia";
import {Friend} from "@/shared/api/types/friend.ts";
import {ref, Ref} from "vue";

export const useFriendsStore = defineStore('friendsStore', () => {
  const friendsList: Ref<Friend[] | null> = ref(null);
  const referralLink: Ref<string> = ref('');
  const sumAllProfits: Ref<number> = ref(0);

  const setFriendsList = (friends: Friend[]) => {
    friendsList.value = friends;
  }

  const setReferralLink = (link: string) => {
    referralLink.value = link;
  }

  const setSumAllProfits = (sum: number) => {
    sumAllProfits.value = sum;
  }

  return {
    friendsList,
    referralLink,
    setFriendsList,
    setReferralLink,
    sumAllProfits,
    setSumAllProfits,
  }
})