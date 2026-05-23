package com.example;

import org.bukkit.block.Block;
import org.bukkit.block.BlockFace;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.event.block.Action;
import org.bukkit.event.player.PlayerInteractEvent;
import org.bukkit.plugin.java.JavaPlugin;
import org.bukkit.util.RayTraceResult;

// Minimal anti-cheat-style validator: on a right-click interaction, raytrace
// from the player's eyes and cancel if the claimed (packet) block+face does not
// match what the player is actually looking at. This is the exact check that
// makes activateBlock's old UP default fail on strict servers (#3851).
public class FaceCheckPlugin extends JavaPlugin implements Listener {
    @Override
    public void onEnable() {
        getServer().getPluginManager().registerEvents(this, this);
        getLogger().info("FaceCheck enabled: claimed interaction face must match eye raytrace");
    }

    @EventHandler
    public void onInteract(PlayerInteractEvent e) {
        if (e.getAction() != Action.RIGHT_CLICK_BLOCK) return;
        Block clicked = e.getClickedBlock();
        if (clicked == null) return;
        BlockFace claimed = e.getBlockFace();
        Player p = e.getPlayer();
        RayTraceResult ray = p.rayTraceBlocks(6.0);
        Block hit = ray == null ? null : ray.getHitBlock();
        boolean sameBlock = hit != null
                && hit.getX() == clicked.getX() && hit.getY() == clicked.getY() && hit.getZ() == clicked.getZ();
        boolean ok = sameBlock && ray.getHitBlockFace() == claimed;
        if (!ok) {
            e.setCancelled(true);
            String got = hit == null ? "nothing" : (hit.getType() + " face " + ray.getHitBlockFace());
            getLogger().warning("[FaceCheck] CANCELLED " + p.getName() + " -> " + clicked.getType()
                    + " claimed face " + claimed + " but eye-raytrace hit " + got);
        } else {
            getLogger().info("[FaceCheck] ALLOWED " + p.getName() + " -> " + clicked.getType() + " face " + claimed);
        }
    }
}
